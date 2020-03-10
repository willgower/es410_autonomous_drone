# ES410 Autonomous Drone
# Owner: James Bennett
# File: main.py
# Description: Module to be entry point and have overall control of companion computer operations

from flight_controller import FlightController
from ground_communication import GroundControlStation
from micro_controller import MicroController
from data_logging import DataLogging
from landing_vision_2 import LandingVision
from recurring_timer import RecurringTimer

import sys
import json
import time
import os
from datetime import datetime as dt
from gpiozero import Button, LED, PWMLED

test = "mission"  # test mode: 'logging', 'take off' or 'mission'


class DroneControl:
    def __init__(self):
        """
        instantiate objects
        this process will establish communication links
        if fail then raise an exception that will terminate the program
        """

        # dictionary of flight parameters
        self.parameters = {
            "descent_vel": 0.25,
            "logging_interval": 0.1
        }

        # Pulse the green LED constantly while script is running
        self.green_led = PWMLED(22)
        self.green_led.pulse(fade_in_time=0.5, fade_out_time=0.5)

        # Flash the red LED if an error occurs
        self.red_led = LED(17)

        # If the button is held for 3 seconds then end the script
        self.button = Button(26)
        self.button.hold_time = 3
        self.button.when_held = self.__prepare_exit

        self.gcs = GroundControlStation()
        if self.gcs.initSuccessful:
            self.report("Link to GCS established")
        else:
            # if fail to open link to GCS no means of reporting so enter specific sequence
            self.alert_initialisation_failure()
            raise ValueError("Failed to communicate with Ground Control Station")

        self.fc = FlightController()
        if self.fc.initSuccessful:
            self.report("Link to FC established")
        else:
            self.report("Link to FC failed")
            raise ValueError("Failed to communicate with Flight Controller")

        self.uC = MicroController()
        if self.uC.initSuccessful:
            self.report("Link to uC established")
        else:
            self.report("Link to uC failed")
            raise ValueError("Failed to communicate with Micro Controller")
        
        self.logger = DataLogging()
        self.vision = LandingVision()
        self.scheduler = RecurringTimer(self.parameters["logging_interval"], self.__monitor_flight)

        # Setting up class attributes
        self.abortFlag = None
        self.emergency_land = False
        self.state = "Initial"
        self.received_mission = None
        self.mission_title = "Default mission name"
        self.reporting_count = 0

    def alert_initialisation_failure(self):
        """
        in case communication to the ground control station (GCS)
        was not established, drone should have other means of reporting initialisation failure
        """
        self.red_led.blink(on_time=0.1, off_time=0.1)

    def report(self, message):
        """
        method to directly report a message to GCS
        """
        self.gcs.send_message(message)
        print(message)

    def abort(self):
        """
        called at any time and will reset drone so in idle state
        """
        self.red_led.blink(on_time=0.1, off_time=0.1, n=25)  # Flash red for 5 seconds while going back to idle
        self.report("Aborting mission...")
        self.abortFlag = True
        self.report("Mission abort successful.")

    def wait_for_command(self):
        """
        drone is in idle state waiting for a command
        return: 0 - shutdown
                1 - mission
                2 - reboot
                else - error so abort
        if mission, then save the mission command as a property
        """
        self.report("Drone is idle. Waiting for command.")

        command = -1
        while command == -1:
            # msg will be type None if no message to read
            msg = self.gcs.read_message()

            if msg == "shutdown":
                command = 0
            elif msg == "reboot":
                command = 2
            elif msg == "mission":
                # mission command recieved, waiting for mission details.
                start = time.perf_counter()

                # timeout after 5 sec
                while time.perf_counter() - start < 5:
                    mission_message = self.gcs.read_message()
                    if mission_message is not None:
                        self.received_mission = json.loads(mission_message)
                        command = 1
                        break
                else:
                    self.report("Wait for mission details timed out after 5 seconds")
                    self.abort()

        return command

    def process_mission(self):
        """
        Processes the received mission and set class attributes
        """
        try:
            self.mission_title = self.received_mission["title"]
            self.fc.set_destination(self.received_mission["location"])
            self.fc.mission_height = int(self.received_mission["altitude"])
        except:
            self.report("Error processing mission, aborting.")
            self.abortFlag = True
        else:
            self.report("Mission processing finished.")

    def battery_load(self):
        """
        loops until battery is loaded
        poll FC to determine if loaded
        timeout after 30 s
        """
        self.report("Waiting for battery to be loaded.")

        # wait for battery connection
        start = time.perf_counter()
        while time.perf_counter() - start < 20:
            if self.fc.is_battery_connected():
                self.report("Battery connected.")
                break
        else:
            self.report("Battery not connected within 20 seconds.")

        # wait for battery secured confirmation
        start = time.perf_counter()
        while time.perf_counter() - start < 20:
            if self.gcs.read_message() == "battery secured":
                self.report("Battery loaded.")
                break
        else:
            self.report("Battery secured confirmation not received within 20 seconds.")

    def parcel_load(self):
        """
        Waits for button press to start parcel load
        """
        # Wait for the button to be pressed
        self.button.wait_for_press()

        # This function is blocking
        self.report("Closing grippers")
        self.uC.close_grippers()

        if self.uC.is_parcel_loaded():
            self.report("Parcel loaded.")
        else:
            self.report("Failed to load parcel.")
            self.abort()

    def check_armable(self):
        """
        do necessary checks to determine if drone is ready to arm
        note, hardware safety switch is pressed after this
        """
        if self.fc.get_armmable_status():
            self.report("Drone ready to arm.")
        else:
            self.report("Arming check failed.")
            self.abort()

    def wait_for_flight_authorisation(self):
        """
        wait for authorisation from ground control station to begin flight
        timeout after 30 s
        """
        self.report("Waiting for authorisation to fly.")
        self.report("Reply \"takeoff\"")

        # wait for message authorising flight - timeout 30 s
        timeout = 30
        start = time.perf_counter()
        while time.perf_counter() - start < timeout:
            if self.gcs.read_message() == "takeoff":
                self.report("Authorisation received.")
                break
        else:
            self.report("Authorisation window timed out.")
            self.abort()

    def execute_flight(self):
        """
        monitor drone status
        facilitate logging
        report to base
        continue when loiter point reached
        """
        # Start data logging
        self.logger.prepare_for_logging(self.mission_title)
        self.scheduler.start()

        self.report("Drone is arming and taking off...")
        self.state = "Arming"
        self.fc.arm()

        # Loop until the drone is almost at traverse altitude
        self.state = "Ascending"
        self.fc.start_ascending()
        while self.fc.get_altitude() < self.fc.mission_height * 0.95:
            time.sleep(0.1)

        # Loop until the drone is within 5m of destination
        self.fc.fly_to_destination()
        self.state = "Traversing"
        while self.fc.get_distance_left() > 5:
            time.sleep(0.1)

        # Loop until the drone is within 2m of ground
        self.fc.change_flight_mode("AUTO")
        self.state = "Descending"
        current_alt = self.fc.get_altitude()
        while current_alt > 2:
            # Use vision system for guidance
            x_vel, y_vel = 1, 2 #  self.vision.get_offset(current_alt)
            z_vel = self.parameters["descent_vel"]
            p_gain = 0.2
            self.fc.move_relative(p_gain * x_vel, p_gain * y_vel, z_vel, 0)
            # Add a delay so that the drone isn't at an angle when the picture is taken
            time.sleep(1)
            current_alt = self.fc.get_altitude()

        # Loop until the drone has landed and is disarmed
        self.state = "Landing"
        self.fc.land()  # This is non blocking
        while self.fc.vehicle.armed:
            drone.report("Drone is landing")
            time.sleep(1)

        drone.report("Drone landed.")

        # Stop data logging
        self.scheduler.stop()
        self.logger.finish_logging()

    def __monitor_flight(self):
        """
        Get flight data from various places and send them to the data logging module
        """

        if self.gcs.read_message() == "emergency land":
            self.fc.vehicle.mode = "LAND"
            while self.fc.vehicle.armed:
                self.report("Drone is executing emergency landing.")
                time.sleep(1)
            self.report("Drone has finished emergency landing.")

            # Then exit the script so operator can approach and turn off the drone
            self.__prepare_exit()

        # Get details to log
        fc_stats = self.fc.get_fc_stats()
        current = self.fc.vehicle.battery.current  # self.uC.get_current() for SITL

        # Send the details to the data logging module
        self.logger.log_info(current, fc_stats)

        # Every second, report the flight stats to the GCS
        if self.reporting_count % 10 == 0:
            message = "State: " + self.state.ljust(10) \
                      + "  |  Altitude: " + fc_stats["Location alt"].ljust(6) \
                      + "  |  Remaining Distance: " + str(round(float(fc_stats["Distance to waypoint"]))).ljust(4) \
                      + "  |  Speed: " + str(round(float(fc_stats["Groundspeed"]), 2)).ljust(5) \
                      + "  |  Battery Voltage (V): " + fc_stats["Battery"].ljust(5) \
                      + "  |  Battery Current (A): " + str(round(float(current))).ljust(5)

            self.report(message)

        self.reporting_count += 1

    def release_package(self):
        """
        open the grippers to release the package
        """
        self.report("Releasing parcel.")
        self.uC.open_grippers()  # blocking function
        self.report("Parcel released.")

    def upload_return_mission(self):
        """
        mission to return to base
        the mission will be executed using previously defined functions
        """
        # Define the return mission
        try:
            self.mission_title += "_return"
            self.fc.set_destination("Post Room")
            # self.fc.mission_height remains the same
        except:
            self.report("Error processing return mission, aborting.")
            self.abortFlag = True
        else:
            self.report("Mission processing finished.")

    def shutdown(self):
        """
        close communication ports and
        perform clean shutdown of electronics running from secondary battery
        """
        self.report("Drone is shutting down.")
        self.__prepare_exit()

        # Shutdown raspberry pi
        os.system('sudo shutdown now')

    def reboot(self):
        """
        close communication ports and reboot drone control components
        good incase we need to reset anything
        """
        self.report("Drone is rebooting.")
        self.__prepare_exit()

        # Reboot raspberry pi
        os.system('sudo shutdown -r now')

    def __prepare_exit(self):
        self.report("Button held - preparing script exit.")

        # Allow modules to cleanly close their processes
        self.logger.close()
        self.uC.close()
        self.fc.close()
        self.gcs.close()

        # Safely exit from GPIO usage
        self.green_led.close()
        self.red_led.close()
        self.button.close()


if test == "mission":
    # === INITIALISATION ===
    # try to initialise drone
    # if fail then print error and exit program
    try:
        drone = DroneControl()
    except ValueError as error:
        print(error)
        sys.exit()
    else:
        drone.report("Initialisation successful.")

    # if exception raised in initialisation then this will not execute because sys.exit()
    while True:
        # === IDLE ===
        # state: idle
        drone.abortFlag = False
        cmd = drone.wait_for_command()

        # === SETTING UP FLIGHT ===
        if cmd == 0:
            drone.shutdown()
        elif cmd == 1:
            drone.process_mission()
        elif cmd == 2:
            drone.reboot()
        else:
            # should never happen
            print("Aborting... Why has this happened?")
            drone.abort()

        # if abort flag is set, stop current iteration and continue with next
        # this sends drone back to idle state
        if drone.abortFlag: continue

        # state: wait for battery load
        drone.battery_load()

        if drone.abortFlag: continue

        # state: wait for parcel load
        drone.parcel_load()

        if drone.abortFlag: continue

        # state: performing arming check
        drone.check_armable()

        if drone.abortFlag: continue

        # pause for 5 seconds to prevent immediate arming
        time.sleep(5)

        if drone.abortFlag: continue

        # state: wait for take off authorisation
        drone.wait_for_flight_authorisation()

        if drone.abortFlag: continue

        # === FLYING ===
        # state: flying
        drone.execute_flight()

        drone.release_package()

        drone.upload_return_mission()

        drone.execute_flight()

        drone.report("Flight complete. Drone at home.")

if test == "logging":
    try:
        drone = DroneControl()
    except ValueError as error:
        print(error)
        sys.exit()
    else:
        drone.report("Initialisation successful.")

    drone.report("Started logging script")

    while True:
        # Wait for the button press to start data logging
        drone.report("Short press for logging. Long press to end script.")
        drone.button.wait_for_press()
        drone.button.wait_for_release()  # Only start logging when it is pressed and released

        # Set up and start logging
        drone.logger.prepare_for_logging(dt.now().strftime("%H-%M-%S_%d-%b"))
        drone.scheduler.start()
        drone.report("Logging started")

        # Add a minimum logging time
        time.sleep(5)

        # Wait for the button press to stop data logging
        drone.button.wait_for_press()
        drone.button.wait_for_release()
        drone.scheduler.stop()
        time.sleep(0.15)
        drone.logger.finish_logging()
        drone.report("Logging stopped")

if test == "take off":
    try:
        drone = DroneControl()
    except ValueError as error:
        print(error)
        sys.exit()
    else:
        drone.report("Initialisation successful.")

    # state: performing arming check
    drone.check_armable()

    # pause for 5 seconds to prevent immediate arming
    time.sleep(5)

    # state: wait for take off authorisation
    drone.wait_for_flight_authorisation()

    # TAKE-OFF TO 3M
    drone.fc.vehicle.simple_takeoff(3)

    alt = drone.fc.get_altitude()
    while alt < 2.75:
        time.sleep(1)
        drone.report("Still ascending. Current altitude: " + alt)
        alt = drone.fc.get_altitude()

    # HOVER FOR 10 SECONDS
    drone.fc.change_flight_mode("LOITER")
    for sec in range(10):
        drone.report("Hovering. Hover time: " + str(sec + 1) + " seconds")

    # LAND
    drone.report("Starting to land")
    drone.fc.land()
    while drone.fc.vehicle.armed:
        drone.report("Drone is landing.")
        time.sleep(1)
    drone.report("Drone has finished landing.")

# ES410 Autonomous Drone
# Owner: James Bennett
# File: main.py
# Description: Module to be entry point and have overall control of companion computer operations

from raspberry_pi.flight_controller import FlightController
from raspberry_pi.ground_communication import GroundControlStation
from raspberry_pi.micro_controller import MicroController
from raspberry_pi.data_logging import DataLogging
from raspberry_pi.landing_vision import LandingVision
from raspberry_pi.recurring_timer import RecurringTimer

import sys
import json
import time
import os


class DroneControl:
    def __init__(self):
        """
        instantiate objects 
        this process will establish communication links
        if fail then raise an exception that will terminate the program
        """

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

        # Setting up class attributes
        self.abortFlag = None
        self.mission_title = ""
		self.state = None

		# dictionary of flight parameters
		self.parameters = {
			"traverse_alt" : 10,

		}

    def alert_initialisation_failure(self):
        """
        in case communication to the ground control station (GCS)
        was not established, drone should have other means of reporting initialisation failure
        """
        # Flash some LEDs!
        # ...for a few seconds then return control to parent function to end program

    def report(self, message):
        """
        method to directly report a message to GCS
        James - is this even required for literally a direct function call? I'd say unnecessary.
        """
        self.gcs.send_message(message)

    def abort(self):
        """
        called at any time and will reset drone so in idle state
        """
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
        self.report("Drone is idle. Waiting for command")

        cmd = -1
        while cmd == -1:
            # msg will be type None if no message to read
            msg = self.gcs.read_message()
            
            if msg == "shutdown":
                cmd = 0
            elif msg == "reboot":
                cmd = 2
            elif msg == "mission":
                # mission command recieved, waiting for mission details.
                missionMessage = None
                start = time.perf_counter()

                # timeout after 5 sec
                while time.perf_counter() - start < 5:
                    missionMessage = self.gcs.read_message()
                    if missionMessage != None: 
                        self.recvdMission = json.loads(missionMessage)
                        cmd = 1
                        break
                else:
                    self.report("Wait for mission details timed out after 5 seconds")
                    self.abort()
                
        return cmd

    def process_mission(self):
        """ 
        This function will sit and wait for a mission to be received from the GCS
        this function must process and set as the mission on the flight controller (FC)
        If the mission requests data logging then it will also need to be triggered here.
        """
        self.mission_title = "Mission Name Here"  # GCS will provide a mission name for logging purposes

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
                self.report("Battery Loaded.")
                break
        else:
            self.report("Battery secured confirmation not received within 20 seconds.")
            self.abort()

    def parcel_load(self):
        """
        loops until parcel is loaded
        on entry, enable parcel load
        check if parcel is loaded
        on exit, disable parcel load
        timeout after 30 s
        """
        
        # open grippers to accept parcel
        self.uC.open_grippers()
        # put in parcel loading mode
        self.uC.set_mode(2)

        # wait until parcel is loaded - timeout 30 s
        self.report("Waiting for parcel to be loaded.")
        timeout = 30
        start = time.perf_counter()
        while time.perf_counter() - start < timeout:
            if self.uC.is_parcel_loaded(): 
                self.report("Parcel Loaded.")
                break
        else:
            self.report("Parcel not loaded within " + timeout + " seconds.")
            self.abort()

    def check_armable(self):
        """
        do necessary checks to determine if drone is ready to arm
        note, hardware safety switch is pressed after this
        """

        ### What other checks should be done?
        # verify battery and package load?
        # verify mission uploaded?

        if not self.fc.get_armable_status():
            self.report("Arming check failed.")
            self.abort()
        else:
            self.report("Drone ready to arm.")

    def wait_for_safety_switch(self):
        """
        loop to until hardware safety switch is pressed
        timeout after 30 s
        """
        self.report("Waiting for hardware safety switch to be pressed.")
        
        # wait for hardware safety switch to be pressed - timeout 30 s
        timeout = 30
        start = time.perf_counter()
        while time.perf_counter() - start < timeout:
            if self.fc.get_hwss_status(): 
                self.report("Switch pressed.")
                break
        else:
            self.report("Switch press timed out.")
            self.abort()

    def wait_for_flight_authorisation(self):
        """
        wait for authorisation from ground control station to begin flight
        timeout after 30 s
        """
        self.report("Waiting for authorisation to fly.")
        
        # wait for message authorising flight - timeout 30 s
        timeout = 30
        start = time.perf_counter()
        while time.perf_counter() - start < timeout:
            if self.gcs.read_message() == "battery secured": 
                self.report("Authorisation received.")
                break
        else:
            self.report("Authorisation window timed out.")
            self.abort()

    def takeoff_and_monitor_flight(self):
        """
        monitor drone status
        facilitate logging
        report to base
        continue when loiter point reached
        """                
        
        self.logger.prepare_for_logging(self.mission_title)
        
        # setup timer
        interval = 1  # second
        # this will start timer also
        self.recTimer = RecurringTimer(interval, self.__monitor_flight)
        
        self.report("Drone is taking off...")
        self.fc.begin_flight()
		self.report("Drone has taken off.")

		# loop until drone is almost at traverse altitude
		self.state = "Ascending"
		while self.fc.get_altitude() < self.parameters["traverse_alt"] * 0.95:
			time.sleep(0.1)

		# loop until drone is almost at traverse altitude
		self.state = "Traversing"
		while self.fc.get_altitude() < self.parameters["traverse_alt"] * 0.95:
			time.sleep(0.1)

        while self.fc.is_drone_at_destination():  # needs to determine when drone is ready for guidance
            # do some stuff
            time.sleep(0.1)

        self.report("Drone at destination. Entering guidance mode.")

    def __monitor_flight(self):
        """
        Get flight data from various places and send them to the data logging module
        """
        # set timer so that it runs recursively
        self.recTimer.start()
        
        # get details to log
        fc_stats = self.fc.get_fc_stats()
        current = self.uC.get_current()

        self.logger.log_info(current, fc_status)

		message = "State: " + self.state + "Altitude :" + fc_stats["Location alt"] + "Distance to waypoint :" + fc_stats[""] + "Battery Voltage (mV): " + fc_stats["Battery"]

        self.report("Drone flying. Progress: ???")

    def guide_to_target(self):
        """
        get drone state
        pass to vision system to compute action
        execute action by instructing FC
        continue logging and reporting
        when above location, land drone
        """
        #
        # do some stuff
        #

        self.report("Initiating landing.")
        self.fc.land()
        self.recTimer.stop()
        self.logger.finish_logging()

    def release_package(self):
        """
        open the grippers to release the package
        """
        self.report("Releasing parcel.")
        self.uC.open_grippers() # blocking function
        self.report("Parcel released.")

    def upload_return_mission(self):
        """
        mission to return to base
        the mission will be executed using previously defined functions
        """

    def shutdown(self):
        """
        close communication ports and 
        perform clean shutdown of electronics running from secondary battery
        """
        self.report("Drone is shutting down.")
        self.__prepare_exit()
        # shutdown raspberry pi
        os.system('sudo shutdown now')

    def reboot(self):
        """
        close communication ports and reboot drone control components
        good incase we need to reset anything
        """
        self.report("Drone is rebooting.")
        self.__prepare_exit()
        # reboot raspberry pi
        os.system('sudo shutdown -r now')

    def __prepare_exit(self):
        self.logger.close()
        self.uC.close()
        self.fc.close()
        self.gcs.close()


if __name__ == "__main__":
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

        # state: wait for hardware safety switch pressed
        drone.wait_for_safety_switch()
        # pause for 5 seconds to prevent immediate arming
        time.sleep(5)

        if drone.abortFlag: continue
        
        # state: wait for take off authorisation
        drone.wait_for_flight_authorisation()

        if drone.abortFlag: continue

        # === FLYING ===
        # state: flying
        drone.takeoff_and_monitor_flight()

        drone.guide_to_target()

        drone.release_package()

        drone.upload_return_mission()

        drone.takeoff_and_monitor_flight()

        drone.guide_to_target()

        drone.report("Flight complete. Drone at home.")
	
    # end while
        





        
    

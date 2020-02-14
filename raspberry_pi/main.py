# ES410 Autonomous Drone
# Owner: James Bennett
# File: main.py
# Description: Module to be entry point and have overall control of companion computer operations

from flight_controller import FlightController
from data_logging import DataLogging
from ground_communication import GroundCommunication
from landing_vision import LandingVision


class DroneControl:
    def __init__(self):
        """
        instantiate objects 
        this process will establish communication links
        """

    def alert_initialisation_failure(self):
        """
        in case communication to the ground control station (GCS) was not established, drone should have other means of reporting initialisation failure
        """

    def report(self, message):
        """
        method to directly report a message to GCS
        """

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
                else - error so abort
        if mission, then save the mission command as a property
        """
        drone.report("Drone is idle. Waiting for command")

        cmd = ""

        return cmd

    def process_mission(self):
        """ 
        when mission received from GCS passed to this fn
        this function must process and set as the mission on the flight controller (FC)
        """

    def battery_load(self):
        """
        loops until battery is loaded
        poll FC to determine if loaded
        timeout after 30 s
        """

    def parcel_load(self):
        """
        loops until parcel is loaded
        on entry, enable parcel load
        check if parcel is loaded
        on exit, disable parcel load
        timeout after 30 s
        """

    def check_armable(self):
        """
        do necessary checks to determine if drone is ready to arm
        note, hardware safety switch is pressed after this
        """

    def wait_for_safety_switch(self):
        """
        loop to until hardware safety switch is pressed
        timeout after 30 s
        """

    def wait_for_flight_authorisation(self):
        """
        wait for authorisation from ground control station to begin flight
        timeout after 30 s
        """

    def takeoff_and_monitor_flight(self):
        """
        monitor drone status
        facilitate logging
        report to base
        continue when loiter point reached
        """

    def guide_to_target(self):
        """
        get drone state
        pass to vision system to compute action
        execute action by instructing FC
        continue logging and reporting
        when above location, land drone
        """

    def release_package(self):
        """
        open the grippers to release the package
        """

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



if __name__=="__main__":
    # initialise drone
    drone = DroneControl()
    # if successful will return drone object
    # else ??????????

    while True:
        # === IDLE ===
        # state: idle
        cmd = drone.wait_for_command()
        
        # === SETTING UP FLIGHT ===
        if cmd == 0:
            drone.shutdown()
        elif cmd == 1:
            drone.process_mission()
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

        drone.takeoff_and_monitor_flight

        drone.guide_to_target()

        drone.report("Flight complete. Drone at home.")

    # end while
        





        
    

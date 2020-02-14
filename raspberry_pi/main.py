# ES410 Autonomous Drone
# Owner: James Bennett
# File: main.py
# Description: Module to be entry point and have overall control of companion computer operations

# do imports

class Main:
    def __init__(self):
        """
        instantiate objects 
        this process will establish communication links
        """

    def alert_initialisation_failure(self):
        """
        in case communication to the ground control station (GCS) was not established, drone should have other means of reporting initialisation failure
        """

    def process_mission(self, missionCmd):
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

    def begin_flight(self):
        """
        issue command to take off
        """

    def monitor_flight(self):
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

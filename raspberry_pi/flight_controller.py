# ES410 Autonomous Drone
# Owner: William Gower
# File: flight_controller.py
# Description: Module to handle MAVLink communication to the Pixhawk


class FlightController:

    def __init__(self):
        """
        Initialise module wide variables and objects.
        """

    def set_destination(self, location):
        """
        Takes in a string of a location from a predefined list.
        E.g. "bluebell", "claycroft", "test_point_A", "test_point_B"
        """

    def land(self):
        """
        Land the drone in the exact position.
        """

    def set_battery_capacity(self, mah):
        """
        Set the size of the battery capacity in mAh.
        """

    def get_fc_status(self):
        """
        Return a json object containing all of the flight controller information
        such as battery level, altitude, GPS, velocity.
        """

    def get_hwss_status(self):
        """
        Get the status of the hardware safety switch
        """

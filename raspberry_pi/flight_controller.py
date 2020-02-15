# ES410 Autonomous Drone
# Owner: William Gower
# File: flight_controller.py
# Description: Module to handle MAVLink communication to the Pixhawk

import dronekit
import socket
import exceptions


class FlightController:

    def __init__(self):
        """
        Initialise module wide variables and objects.
        Start MAVLink connection to the Pixhawk
        Set flag for successful initialisation
        """
        self.initSuccessful = False  # Assume connection fails
        try:
            dronekit.connect('/dev/serial/by-id/usb-ArduPilot_fmuv2_390030000E51373337333031', heartbeat_timeout=15)
        except socket.error:  # Bad TCP connection
            print('No server exists!')
        except exceptions.OSError as e:  # Bad TTY connection
            print('No serial exists!')
        except dronekit.APIException:  # API Error
            print('Timeout!')
        except:  # Other error
            print('Some other error!')
        else:
            self.initSuccessful = True

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
        Get the status of the hardware safety switch.
        """

    def get_arm_status(self):
        """
        Return whether or not the drone is armable.
        """

    def begin_flight(self):
        """
        Run the take off and mission starting commands.
        """

    def change_flight_mode(self, flight_mode):
        """
        Change between auto mission mode and guided 'joystick' mode.
        """

    def move_relative(self, x, y, altitude, yaw):
        """
        Provide low level 'joystick style' commands to the drone.
        """


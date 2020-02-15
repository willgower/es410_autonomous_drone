# ES410 Autonomous Drone
# Owner: William Gower
# File: flight_controller.py
# Description: Module to handle MAVLink communication to the Pixhawk

import dronekit
from pymavlink import mavutil
import socket
import json

class FlightController:
    def __init__(self):
        """
        Initialise module wide variables and objects.
        Start MAVLink connection to the Pixhawk
        Set flag for successful initialisation
        /dev/serial/by-id/usb-ArduPilot_fmuv2_390030000E51373337333031
        """
        self.initSuccessful = False  # Assume connection fails
        try:
            self.vehicle = dronekit.connect('/dev/ttyACM0', heartbeat_timeout=15)
            print("Successfully connected to Pixhawk!")
        except socket.error:  # Bad TCP connection
            print('No server exists!')
            return
        except OSError as e:  # Bad TTY connection
            print('No serial exists!')
            return
        except dronekit.APIException:  # API Error
            print('Timeout!')
            return
        except:  # Other error
            print('Some other error!')
            return
        else:
            self.initSuccessful = True

        self.vehicle.mode = 'AUTO'

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
        fc_data = {
            "Global Location": str(self.vehicle.location.global_frame),
            "Velocity": str(self.vehicle.velocity),
            "GPS": str(self.vehicle.gps_0),
            "Battery": str(self.vehicle.battery),
            "Groundspeed": str(self.vehicle.groundspeed),
            "Airspeed": str(self.vehicle.airspeed)
        }

        fc_data_encoded = json.JSONEncoder().encode(fc_data)

        return fc_data_encoded

    def get_hwss_status(self):
        """
        Get the status of the hardware safety switch.
        """
        return self.vehicle.

    def get_arm_status(self):
        """
        Return whether or not the drone is armable.
        """
        return self.vehicle.is_armable

    def begin_flight(self):
        """
        Run the take off and mission starting commands.
        """

    def change_flight_mode(self, flight_mode):
        """
        Change between auto mission mode and guided 'joystick' mode.
        """
        if flight_mode in ["AUTO", "GUIDED", "LOITER"]:
            self.vehicle.mode = flight_mode
        else:
            print("Invalid flight mode sent")

    def move_relative(self, velocity_x, velocity_y, velocity_z, yaw):
        """
        Provide low level 'joystick style' commands to the drone.
        """
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0,                                              # time_boot_ms (not used)
            0, 0,                                           # target_system, target_component
            mavutil.mavlink.MAV_FRAME_BODY_NED,   # frame
            0b0000111111000111,                             # type_mask (only speeds enabled)
            0, 0, 0,                                        # x, y, z positions
            velocity_x, velocity_y, velocity_z,             # x, y, z velocity in m/s
            0, 0, 0,                                        # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
            0, 0)                                           # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

        self.vehicle.send_mavlink(msg)  # Send the command to the vehicle


if __name__ == "__main__":
    fc = FlightController()
    if fc.initSuccessful:
        fc.get_fc_status()
    else:
        quit()

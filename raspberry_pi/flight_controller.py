# ES410 Autonomous Drone
# Owner: William Gower
# File: flight_controller.py
# Description: Module to handle MAVLink communication to the Pixhawk

import dronekit
import socket


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
        self.vehicle.wait_ready('autopilot_version')

        # Get all vehicle attributes (state)
        print("\nGet all vehicle attribute values:")
        print(" Autopilot Firmware version: %s" % self.vehicle.version)
        print("   Major version number: %s" % self.vehicle.version.major)
        print("   Minor version number: %s" % self.vehicle.version.minor)
        print("   Patch version number: %s" % self.vehicle.version.patch)
        print("   Release type: %s" % self.vehicle.version.release_type())
        print("   Release version: %s" % self.vehicle.version.release_version())
        print("   Stable release?: %s" % self.vehicle.version.is_stable())
        print(" Autopilot capabilities")
        print("   Supports MISSION_FLOAT message type: %s" % self.vehicle.capabilities.mission_float)
        print("   Supports PARAM_FLOAT message type: %s" % self.vehicle.capabilities.param_float)
        print("   Supports MISSION_INT message type: %s" % self.vehicle.capabilities.mission_int)
        print("   Supports COMMAND_INT message type: %s" % self.vehicle.capabilities.command_int)
        print("   Supports PARAM_UNION message type: %s" % self.vehicle.capabilities.param_union)
        print("   Supports ftp for file transfers: %s" % self.vehicle.capabilities.ftp)
        print("   Supports commanding attitude offboard: %s" % self.vehicle.capabilities.set_attitude_target)
        print(
            "   Supports commanding position and velocity targets in local NED frame: %s" % self.vehicle.capabilities.set_attitude_target_local_ned)
        print(
            "   Supports set position + velocity targets in global scaled integers: %s" % self.vehicle.capabilities.set_altitude_target_global_int)
        print("   Supports terrain protocol / data handling: %s" % self.vehicle.capabilities.terrain)
        print("   Supports direct actuator control: %s" % self.vehicle.capabilities.set_actuator_target)
        print("   Supports the flight termination command: %s" % self.vehicle.capabilities.flight_termination)
        print("   Supports mission_float message type: %s" % self.vehicle.capabilities.mission_float)
        print("   Supports onboard compass calibration: %s" % self.vehicle.capabilities.compass_calibration)
        print(" Global Location: %s" % self.vehicle.location.global_frame)
        print(" Global Location (relative altitude): %s" % self.vehicle.location.global_relative_frame)
        print(" Local Location: %s" % self.vehicle.location.local_frame)
        print(" Attitude: %s" % self.vehicle.attitude)
        print(" Velocity: %s" % self.vehicle.velocity)
        print(" GPS: %s" % self.vehicle.gps_0)
        print(" Gimbal status: %s" % self.vehicle.gimbal)
        print(" Battery: %s" % self.vehicle.battery)
        print(" EKF OK?: %s" % self.vehicle.ekf_ok)
        print(" Last Heartbeat: %s" % self.vehicle.last_heartbeat)
        print(" Rangefinder: %s" % self.vehicle.rangefinder)
        print(" Rangefinder distance: %s" % self.vehicle.rangefinder.distance)
        print(" Rangefinder voltage: %s" % self.vehicle.rangefinder.voltage)
        print(" Heading: %s" % self.vehicle.heading)
        print(" Is Armable?: %s" % self.vehicle.is_armable)
        print(" System status: %s" % self.vehicle.system_status.state)
        print(" Groundspeed: %s" % self.vehicle.groundspeed)  # settable
        print(" Airspeed: %s" % self.vehicle.airspeed)  # settable
        print(" Mode: %s" % self.vehicle.mode.name)  # settable
        print(" Armed: %s" % self.vehicle.armed)  # settable

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


if __name__ == "__main__":
    fc = FlightController()
    fc.get_fc_status()

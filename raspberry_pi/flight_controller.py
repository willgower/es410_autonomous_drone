# ES410 Autonomous Drone
# Owner: William Gower
# File: flight_controller.py
# Description: Module to handle MAVLink communication to the Pixhawk

import dronekit
from pymavlink import mavutil
import socket
import time
import os


class FlightController:
    def __init__(self):
        """
        Initialise module wide variables and objects.
        Start MAVLink connection to the Pixhawk
        Set flag for successful initialisation
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

        self.vehicle.mode = 'AUTO'  # Set the default vehicle mode

        self.locations = {}
        with open(os.path.dirname(os.path.abspath(__file__)) + '/locations.txt', 'r') as file:
            for line in file.readlines():
                name = line[:line.find(":")].strip()
                lat = line[line.find(":") + 2:line.find(",")].strip()
                long = line[line.find(",") + 1:].strip()
                self.locations[name] = (lat, long)

        self.mission_lat = None
        self.mission_lon = None

    def set_destination(self, location):
        """
        Takes in a string of a location from a predefined list.
        E.g. "bluebell", "claycroft", "test_point_A", "test_point_B"
        """
        self.mission_lon = self.locations[location][0]
        self.mission_lat = self.locations[location][1]

    def land(self):
        """
        Land the drone in the exact position.
        """
        self.vehicle.mode = "LAND"

    def is_drone_at_destination(self):
        """
        added by JRB
        please return true or false
        this is to allow drone to go into guided state
        """

    def set_battery_capacity(self, mah):
        """
        Set the size of the battery capacity in mAh.
        """

    def is_battery_connected(self):
        """
        Returns true or false if the battery is connected
        """
        if self.vehicle.battery[0] is not None:  # This might not work - needs testing!
            return True
        else:
            return False

    def get_fc_stats(self):
        """
        Return a dictionary containing all of the flight controller information including:
            - Global Location
            - Velocity
            - GPS
            - Battery voltage
            - Groundspeed
            - Airspeed
        """
        fc_data = {
            "Location lon": str(self.vehicle.location.global_frame.lon),
            "Location lat": str(self.vehicle.location.global_frame.lat),
            "Location alt": str(self.vehicle.location.global_frame.alt),
            "Range Finder Height": str(self.vehicle.rangefinder),
            "Distance to waypoint": str(0),
            "Velocity": str(self.vehicle.velocity),
            "Displacement": str(0),
            "Battery": str(self.vehicle.battery.voltage),
            "Groundspeed": str(self.vehicle.groundspeed),
            "Airspeed": str(self.vehicle.airspeed)
        }

        # fc_data_encoded = json.JSONEncoder().encode(fc_data)

        return fc_data

    def get_hwss_status(self):
        """
        Get the status of the hardware safety switch.
        Return true if pressed
        """

    def get_armmable_status(self):
        """
        Return whether or not the drone is armable.
        """
        return self.vehicle.is_armable

    def begin_flight(self):
        """
        Run the take off and mission starting commands.
        """
        # Copter should arm in GUIDED mode
        self.vehicle.mode = "GUIDED"
        self.vehicle.armed = True

        while not self.vehicle.armed:
            time.sleep(1)

        self.vehicle.simple_takeoff(10)  # Take off to 9m

    def fly_to_location(self):
        """
        Start the traversing stage of flight
        """
        location = dronekit.LocationGlobalRelative(self.mission_lat,  # Mission latitude
                                                   self.mission_lon,  # Mission longitude
                                                   10                 # Mission altitude
                                                   )
        self.vehicle.simple_goto(location)

    def get_distance_left(self):
        """
        Return the horizontal distance to the next waypoint
        """

    def get_altitude(self):
        """
        Returns the current flight altitude
        """
        return self.vehicle.location.global_frame.alt

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
            0, 0, 0,                                        # x, y, z acceleration (not supported yet)
            0, 0)                                           # yaw, yaw_rate (not supported yet)

        self.vehicle.send_mavlink(msg)  # Send the command to the vehicle

    def close(self):
        """
        prepare for system shutdown
        stop processes, close communications and shutdown hardware where possible
        """
        self.vehicle.close()


if __name__ == "__main__":
    fc = FlightController()
    if fc.initSuccessful:
        print(fc.get_fc_status())
    else:
        quit()

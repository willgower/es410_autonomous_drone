# ES410 Autonomous Drone
# Owner: William Gower
# File: data_logging.py
# Description: Module to handle the logging of in flight data such as current readings against time.

from datetime import datetime
import serial
import json
import os


class DataLogging:
    def __init__(self):
        self.currently_logging = False
        self.file_path = os.getcwd() + "/logging/"
        self.data_file = None

    def prepare_for_logging(self, name):
        """
        open file
        write a header
        """
        self.currently_logging = True
        self.data_file = open(self.file_path + name + ".csv", "w+")
        self.data_file.write("Logging started at " + datetime.now().strftime("%d-%m-%y at %H:%M:%S\n"))
        self.data_file.write("Longitude, Latitude, Altitude, Velocity, Groundspeed, Airspeed, Current, Voltage\n")

    def log_info(self, current, fc_data_in):
        """
        function should save information to a file in appropriate format
        """

        data = {"Location lon": fc_data_in["Location lon"],
                "Location lat": fc_data_in["Location lat"],
                "Location alt": fc_data_in["Location alt"],
                "Velocity": fc_data_in["Location lat"],
                "Ground Speed": fc_data_in["Groundspeed"],
                "Airspeed": fc_data_in["Airspeed"],
                "Current": str(current),
                "Voltage": fc_data_in["Battery"]}

        self.data_file.write(', '.join(data.values()) + "\n")
        
    def finish_logging(self):
        """
        flight finished, close file
        """
        self.data_file.close()
        self.currently_logging = False

    def close(self):
        """
        prepare for system shutdown
        If logging hasn't already been stopped - do this now
        """
        if self.currently_logging:
            self.finish_logging()


if __name__ == "__main__":
    from random import random, choice
    from math import floor

    data_logging = DataLogging()
    data_logging.prepare_for_logging("test_2")
    for x in range(10):
        fc_data = {"voltage": str(x * 10),
                   "location": str(floor(100 * random())),
                   "velocity": choice(["fast", "slow", "average"])}
        data_logging.log_info(x + 1, json.JSONEncoder().encode(fc_data))
    data_logging.finish_logging()

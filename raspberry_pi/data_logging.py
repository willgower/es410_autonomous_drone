# ES410 Autonomous Drone
# Owner: William Gower
# File: data_logging.py
# Description: Module to handle the logging of in flight data such as current readings against time.

from datetime import datetime as dt
import json
import os
from gpiozero import LED


class DataLogging:
    def __init__(self):
        self.currently_logging = False
        self.data_file = None
        self.blue_led = LED(27)

    def prepare_for_logging(self, name):
        """
        open file
        write a header
        """
        self.currently_logging = True

        try:  # Memory stick first
            os.system("sudo mount /dev/disk/by-uuid/0177-74FD /media/usb_logger")
            self.data_file = open("/media/usb_logger/" + name + ".csv", "w+")
        except:  # Try locally on the Pi
            self.data_file = open(os.path.dirname(os.path.abspath(__file__)) + "/logging/" + name + ".csv", "w+")

        self.data_file.write("Logging started at " + dt.now().strftime("%d-%m-%y at %H:%M:%S\n"))
        self.data_file.write("Timestamp, Longitude, Latitude, Altitude, Velocity, "
                             "Groundspeed, Airspeed, Current, Voltage\n")

    def log_info(self, current, fc_data_in):
        """
        function should save information to a file in appropriate format
        """
        self.blue_led.blink(on_time=0.05, n=1)

        data = {"Timestamp": dt.now().strftime("%H:%M:%S.%f"),
                "Location lon": fc_data_in["Location lon"],
                "Location lat": fc_data_in["Location lat"],
                "Location alt": fc_data_in["Location alt"],
                "Velocity": fc_data_in["Velocity"],
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
        try:
            os.system("sudo umount /media/usb_logger")
        except:
            pass
        self.currently_logging = False

    def close(self):
        """
        prepare for system shutdown
        If logging hasn't already been stopped - do this now
        """
        if self.currently_logging:
            self.finish_logging()
        self.blue_led.close()


def log_random():
    data = {"Timestamp": dt.now().strftime("%H:%M:%S.%f"),
            "Location lon": "Location lon",
            "Location lat": "Location lat",
            "Location alt": "Location alt",
            "Velocity": str(randint(1, 10)),
            "Groundspeed": str(randint(1, 10)),
            "Airspeed": str(randint(1, 10)),
            "Battery": str(randint(14, 17))}

    data_logging.log_info(90, data)


if __name__ == "__main__":
    from random import randint
    from recurring_timer import RecurringTimer
    import time

    scheduler = RecurringTimer(0.1, log_random)
    data_logging = DataLogging()
    data_logging.prepare_for_logging("test_bench")

    scheduler.start()
    print("Logging started")

    # Add a minimum logging time
    time.sleep(5)

    while True:
        if input("Hit enter to finish logging!") == "":
            scheduler.stop()
            data_logging.finish_logging()
            print("Logging stopped")
            break

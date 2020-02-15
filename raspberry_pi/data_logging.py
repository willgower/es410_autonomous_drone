# ES410 Autonomous Drone
# Owner: William Gower
# File: data_logging.py
# Description: Module to handle the logging of in flight data such as current readings against time.

from threading import Timer
from datetime import datetime
import serial


class DataLogging:
    def __init__(self):
        self.file_path = "logging/"
        self.data_file = None
        self.t = None
        self.started = False
        self.delay = None

        self.ser = serial.Serial("/dev/ttyUSB0", 115200)
        self.ser.baudrate = 115200

    def start(self, name, delay=0.25):
        self.started = True
        self.delay = delay
        self.data_file = open(self.file_path + name + ".csv", "w")
        self.data_file.write("Logging started at " + datetime.now().strftime("%d-%m-%y at %H:%M:%S\n"))
        self.log_new_sample()

    def log_new_sample(self):
        read_ser = self.ser.readline().strip().decode('ascii')
        if read_ser:
            c_time = datetime.now().strftime("%H:%M:%S.%f")
            current, voltage, location = read_ser.split(',')
            velocity = "speed"
            altitude = str(20)

            sample = ",".join([c_time, current, voltage, location, velocity, altitude]) + "\n"
        else:
            sample = "None," * 6

        self.data_file.write(sample)

        self.t = Timer(self.delay, self.log_new_sample)
        self.t.start()

    def stop(self):
        if not self.started:
            return
        self.t.cancel()
        self.data_file.close()

    def close(self):
        """
        prepare for system shutdown
        Will - or does the above method do this?
        """


if __name__ == "__main__":
    data_logging = DataLogging()
    data_logging.start("next", 0.1)
    time.sleep(5)
    data_logging.stop()

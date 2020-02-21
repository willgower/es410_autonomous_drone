# ES410 Autonomous Drone
# Owner: William Gower
# File: micro_controller.py
# Description: Module to handle serial connection to the Arduino

import serial
import time


class MicroController:
    def __init__(self):
        """
        establish communication to arduino (timeout = 5 s)
        get confirmation from arduino that grippers are open
        Set flag for successful initialisation
        """

        self.ser = serial.Serial("/dev/ttyACM1", 9600)
        self.ser.baudrate = 9600
        self.ser.timeout = 0.1

        while not self.ser.is_open:
            time.sleep(1)

        self.initSuccessful = True

    def set_mode(self, mode):
        """
        send message to arduino to put into specified mode
        mode:   0 - idle (arduino reads serial port awaiting instruction)
                1 - current measuring
                2 - enable parcel load (grippers closing)
                3 - open grippers
        """

    def is_parcel_loaded(self):
        """
        non-blocking function to return true or false
        """

    def open_grippers(self):
        """
        first, set mode to 3
        then read serial port in a loop until message that grippers are open
        """

    def get_current(self):
        """
        when called should return latest current reading
        """
        try:
            self.ser.reset_input_buffer()
            self.ser.readline()
            read_ser = self.ser.readline().strip().decode('ascii')
        except:
            read_ser = "Failed to get current reading"

        return read_ser

    def close(self):
        """
        prepare for system shutdown
        stop processes, close communications and shutdown hardware where possible
        """
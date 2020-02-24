# ES410 Autonomous Drone
# Owner: William Gower
# File: micro_controller.py
# Description: Module to handle serial connection to the Arduino

import serial
import time


class MicroController:
    def __init__(self):
        """
        establish communication to arduino
        Set flag for successful initialisation
        """
        try:
            self.ser = serial.Serial("/dev/serial/by-id/usb-Arduino_LLC_Arduino_Nano_Every_C2AD5E5651514743594A2020FF054A1D-if00", 9600)  # /dev/ttyACM0
            self.ser.baudrate = 9600
            self.ser.timeout = 0.1
        except:
            self.initSuccessful = False
        else:
            self.initSuccessful = True

    def set_mode(self, mode):
        """
        send message to arduino to put into specified mode
        mode:   0 - idle (arduino reads serial port awaiting instruction)
                1 - current measuring
                2 - enable parcel load (grippers closing)
                3 - open grippers
        """
        self.ser.write("mode" + str(mode))

    def is_parcel_loaded(self):
        """
        non-blocking function to return true or false
        """
        if self.ser.readline() == "complete":
            self.ser.write("received")
            return True
        else:
            return False

    def open_grippers(self):
        """
        first, set mode to 3
        then read serial port in a loop until message that grippers are open
        """
        self.set_mode(3)
        while self.ser.readline() != "complete":
            time.sleep(0.1)
            self.ser.reset_input_buffer()
        self.ser.write("received")

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
        self.ser.flush()
        self.ser.close()

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

        self.parcel_loaded = False  # When powered on there will be no package

    def set_mode(self, mode):
        """
        send message to arduino to put into specified mode
        mode:   0 - idle (arduino reads serial port awaiting instruction)
                1 - current measuring
                2 - enable parcel load (grippers closing)
                3 - open grippers
        """
        self.ser.write(str(mode).encode('utf-8'))

    def is_parcel_loaded(self):
        """
        non-blocking function to return true or false
        """
        return self.parcel_loaded

    def close_grippers(self):
        """
        first, set mode to 2
        then read serial port in a loop until message that grippers are closed
        """
        self.set_mode(2)

        """
        while self.ser.readline() != "grippers_closed":
            self.ser.reset_input_buffer()
            time.sleep(0.1)
        self.parcel_loaded = True
        """

        # Mimic this taking 2 seconds for now
        time.sleep(2)
        self.parcel_loaded = True

    def open_grippers(self):
        """
        first, set mode to 3
        then read serial port in a loop until message that grippers are open
        """
        self.set_mode(3)
        while self.ser.readline() != "grippers_opened":
            self.ser.reset_input_buffer()
            time.sleep(0.1)
        self.parcel_loaded = False

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

# ES410 Autonomous Drone
# Owner: William Gower
# File: micro_controller.py
# Description: Module to handle serial connection to the Arduino


class MicroController:
    def __init__(self):
        """
        establish communication to arduino (timeout = 5 s)
        get confirmation from arduino that grippers are open
        Set flag for successful initialisation
        """
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

    def close(self):
        """
        prepare for system shutdown
        stop processes, close communications and shutdown hardware where possible
        """
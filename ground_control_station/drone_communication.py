# ES410 Autonomous Drone
# Owner: William Gower
# File: ground_communication.py
# Description: Module to handle serial communication to the ground control station

class DroneComms:
    def __init__(self):
        """
        start wireless serial connection to drone
        """

    def read_message(self):
        """
        Read the latest message from the serial buffer and return it
        Will - is this going to return None if no message read?
        """

    def send_message(self, message):
        """
        Send message to drone
        """

    def close(self):
        """
        do we need to close this link from the GCS?
        """

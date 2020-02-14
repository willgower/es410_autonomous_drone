# ES410 Autonomous Drone
# Owner: William Gower
# File: ground_communication.py
# Description: Module to handle serial communication to the ground control station


class GroundCommunication:
    def __init__(self):
        """
        Start wireless serial connection to the GCS using the NRF24L01 modules.
        Timeout - 10s
        """

    def read_message(self):
        """
        Read the latest message from the serial buffer and return it
        """

    def send_message(self):
        """
        Send the message back to the GCS
        """

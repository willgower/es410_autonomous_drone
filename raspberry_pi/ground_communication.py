# ES410 Autonomous Drone
# Owner: William Gower
# File: ground_communication.py
# Description: Module to handle serial communication to the ground control station

from gpiozero import LED
import serial


class GroundControlStation:
    def __init__(self):
        """
        Start wireless serial connection to the GCS using the NRF24L01 modules.
        Timeout - 10s
        """
        
        self.initSuccessful = True

        self.yellow_led = LED(4)
        # Start serial connection here as soon as module is instantiated

    def read_message(self):
        """
        Read the latest message from the serial buffer and return it without:
            - whitespace
            - carriage return
            - new line
        """

    def send_message(self, message):
        """
        Send the message back to the GCS
        """
        self.yellow_led.blink(on_time=0.05, off_time=0.05, n=20)  # Flash quick for 1 second when sending a message

    def close(self):
        """
        prepare for system shutdown
        stop processes, close communications and shutdown hardware where possible
        """


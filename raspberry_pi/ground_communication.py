# ES410 Autonomous Drone
# Owner: William Gower
# File: ground_communication.py
# Description: Module to handle serial communication to the ground control station

# =============== NOTES ===============
# → skeleton completed by JRB so DroneControl can be written
#
# =====================================

class GroundControlStation:

    def __init__(self):
        """
        Start wireless serial connection to the GCS using the NRF24L01 modules.
        Timeout - 10s
        """
        
        self.initSuccessful = True
        
        # Start serial connection here as soon as module is instantiated

    def read_message(self):
        """
        Read the latest message from the serial buffer and return it
        """

    def send_message(self, message):
        """
        Send the message back to the GCS
        """


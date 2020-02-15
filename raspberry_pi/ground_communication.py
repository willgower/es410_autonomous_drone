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
        open communication to ground station 
        handle errors
        Set flag for successful initialisation
        """

        self.initSuccessful = True

    def read_msg(self):
        """
        read ground control station
        return message as string
        """

    def send_msg(self, msg):
        """
        send specified message to the GCS
        """
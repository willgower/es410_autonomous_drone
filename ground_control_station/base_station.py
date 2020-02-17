# ES410 Autonomous Drone
# Owner: James Bennett
# File: base_station.py
# Description: File to run locally on a laptop acting as the ground control station.

from ground_control_station.drone_communication import DroneComms


class BaseStation:
    def __init__(self):
		 """
		 start communcation with drone
		 """
		 
		 self.drone = DroneComms()






if __name__=="__main__":
	try:
		
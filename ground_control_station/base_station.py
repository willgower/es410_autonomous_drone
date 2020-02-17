# ES410 Autonomous Drone
# Owner: James Bennett
# File: base_station.py
# Description: File to run locally on a laptop acting as the ground control station.

from ground_control_station.drone_communication import DroneComms
import sys

class BaseStation:
    def __init__(self):
		 """
		 start communcation with drone
		 """
		 
		 self.drone = DroneComms()






if __name__=="__main__":
	while True:
		# trying to connect to drone
		try:
			base = BaseStation()
		except:
			print("Failed to connect to drone.")
			reponse = input("Would you like to try again? (y/n)")
			if response == 'y':
				continue
			elif response == 'n':
				break

	# after while loop, exit program
	sys.exit()
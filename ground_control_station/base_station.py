# ES410 Autonomous Drone
# Owner: James Bennett
# File: base_station.py
# Description: File to run locally on a laptop acting as the ground control
# station.

from drone_communication import DroneComms
import sys
import os
import json
import time


def wait_for_msg(message):
	"""
	prints messages from drone until specified message is received
	does not print specified message
	"""
	msg = None
	while msg != message:
		if not msg == None:
			print("   Message from drone: " + msg)
		msg = drone.read_message()

def verify(action):
	print("Are you sure you want to " + action + "?")
	ans = input("Response (y/n): ")
	while ans not in ('y', 'n'):
		print("Response not recognised. Try again.")
		ans = input("Response (y/n): ")
	return ans 

if __name__ == "__main__":
	while True:
        # === DRONE STATE: INITIALISING ===
		# trying to connect to drone
		print("Trying to connect to drone...")
		try:
			drone = DroneComms()
		except:
			print("Failed to connect to drone. Would you like to try again?")
			response = input("Response (y/n): ")
			if response == 'y':
				continue
			elif response == 'n':
				break
		else:
			print("Connection established. Waiting for drone to initialise...")

        # waiting for initialisation to be complete
		wait_for_msg("Initialisation successful.")
		print("Drone Initialisation Complete.\n")
		break

	while True:
		# === DRONE STATE: IDLE ===
		print("Drone idle. Waiting for command.")
		command = input("Enter command: ")
		# --- shutdown ---
		if command == "shutdown":
			answer = verify("shutdown")
			if answer == 'y':
				drone.send_message("shutdown")
				wait_for_msg("Drone is shutting down.")
				print("Drone shutting down.")
				while drone.is_comms_open():
					# use this to verify drone is shutting down.
					continue
				print("Connection to drone lost. Exiting program.")
				sys.exit()
			elif answer == 'n':
				time.sleep(1)
				continue # go back to idle state
			else: # problem
				print("Problem. This shouldn't have happend. Quitting.")
				sys.exit()
		
		# --- reboot ---
		elif command == "reboot":
			answer = verify("reboot")
			if answer == 'y':
				drone.send_message("reboot")
				wait_for_msg("Drone is rebooting.")
				print("Drone rebooting.")
				while drone.is_comms_open():
					# use this to verify drone is shutting down.
					continue
				print("Connection to drone lost. Exiting program.")
				sys.exit()
			elif answer == 'n':
				time.sleep(1)
				continue # go back to idle state
			else: # problem
				print("Problem. This shouldn't have happend. Quitting.")
				sys.exit()

		# --- mission ---
		elif command == "mission":
			print("Please enter the mission details.")
			# store values in a dictionary then send encoded as json
			mission = {}
			mission["title"] = input("  Mission Title: ")
			#
			# enter more mission details here
			#

			# encode mission as json
			str_mission = json.dumps(mission)
			# send "mission" to put drone in state ready to receive mission details
			drone.send_message("mission")
			# send mission details
			drone.send_message("str_mission")

			print("Mission sent. Drone is processing the mission. Please wait.")
			wait_for_msg("Mission processing finished.")
			print("Mission upload complete. \n")

		# === DRONE STATE: BATTERY LOADING ===
		print("Please load battery into the drone.")
		wait_for_msg("Battery connected.")
		print("Battery is connected. Please confirm the battery is secured.")
		response = get_response("Is battery secured (y/n): ")


	# after while loop, exit program
	quit()
# ES410 Autonomous Drone
# Owner: James Bennett
# File: base_station.py
# Description: File to run locally on a laptop acting as the ground control
# station.

from ground_control_station.drone_communication import DroneComms  # hmm odd behaviour regarding folder name
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
	return get_response("Response (y/n): ")
	 
def get_response(prompt):
	ans = input(prompt)
	while ans not in ('y', 'n'):
		print("Response not recognised. Try again.")
		ans = input(prompt)
	return ans

def abort_setup():
	print("\n Aborting setup. Please wait for drone to timeout and be ready to receive a command. \n")
	time.sleep(3)
	os.system("clear")

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
		print("Waiting for drone to confirm it is ready for a command...")
		wait_for_msg("Drone is idle. Waiting for command.")  # this line mainly if user responds no
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
				abort_setup()
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
				abort_setup()
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
		if response == 'y':
			drone.send_message("battery secured")
			wait_for_msg("Battery Loaded.")
			print("Battery load complete. \n")
		elif response == 'n':
			abort_setup()
			continue # go back to idle state
		else: # problem
			print("Problem. This shouldn't have happend. Quitting.")
			sys.exit()

		# === DRONE STATE: PARCEL LOADING ===
		print("Please hold parcel underneath drone and press button to close the grippers.")
		wait_for_msg("Parcel loaded.")
		
		# === DRONE STATE: CHECK DRONE IS ARMABLE ===
		print("Checking drone is armable.")
		wait_for_msg("Drone ready to arm.")
		print("Drone is ready to arm. \n")

		# === DRONE STATE: WAITING FOR HWSS ===
		print("Please press the hardware safety switch.")
		wait_for_msg("Switch pressed.")
		print("Switch pressed. Pausing to allow all people to withdraw to a safe distance. \n")

		# === DRONE STATE: WAITING FOR FLIGHT AUTHORISATION ===
		wait_for_msg("Waiting for authorisation to fly.")
		print("Drone is ready to fly. Awaiting authorisation to begin flight.")
		print(" **WARNING: when you grant authorisation the drone will take off. Ensure it is safe to begin flight.** ")
		print("Enter ""takeoff"" to begin the flight or ""cancel"" to abort")
		
		command = input("Command: ")
		while command not in ('takeoff', 'cancel'):
			print("Response not recognised, please enter ""takeoff"" or ""cancel""")
			command = input("Command: ")
		
		if command == "takeoff":
			drone.send_message("takeoff")
			wait_for_msg("Authorisation received.")
			print("Authorisation received by drone. Beginning flight imminently")
			# continue with program
		elif command == "cancel":
			ababort_setup()
			continue # go back to idle state
		else: # problem
			print("Problem. This shouldn't have happend. Quitting.")
			sys.exit()
		
		# === DRONE STATE: FLYING ===
		print("Drone is in flight mode. Messages from drone will be reported.")
		msg = None
		while msg != "Flight complete. Drone at home.":
			if not msg == None:
				print("  " + msg)
			msg = drone.read_message()

	# after while loop, exit program
	quit()
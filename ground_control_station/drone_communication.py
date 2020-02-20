# ES410 Autonomous Drone
# Owner: William Gower
# File: ground_communication.py
# Description: Module to handle serial communication to the drone from the GCS

import time

class DroneComms:
	def __init__(self):
		"""
		start wireless serial connection to drone
		"""
		time.sleep(1)
		#raise Exception()

	def read_message(self):
		"""
		Read the latest message from the serial buffer and return it
		Will - is this going to return None if no message read?
		"""
		# for debug
		inpt = input("> Drone says: ")
		return inpt

	def send_message(self, message):
		"""
		Send message to drone
		"""

	def is_comms_open(self):
		"""
		Will - in the event of a shutdown/reboot I would like to know 
		when the communication link has failed (as verification the drone has shut down)
		it seems if you create the serial object ser = serial.Serial()
		you can do ser.is_open - though I expect I don't need to tell you this
		"""
		
		return False # for debug

	def close(self):
		"""
		do we need to close this link from the GCS?
		"""

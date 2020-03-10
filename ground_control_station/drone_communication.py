# ES410 Autonomous Drone
# Owner: William Gower
# File: drone_communication.py
# Description: Module to handle serial communication to the drone from the GCS

import serial
import platform
import calendar
import time


class DroneComms:
	def __init__(self):
		"""
		Start wireless serial connection to drone
		"""
		if platform.system() == "Linux":
			# Start a serial connection on a Linux laptop
			self.ser = serial.Serial(
				"/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0",
				# Depends which UART -> USB converter is being used
				# '/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_55739323437351811190-if00',
				baudrate=9600,
				timeout=0.05)
		elif platform.system() == "Windows":
			# Start a serial connection with a Windows laptop
			self.ser = serial.Serial(
				input("Enter COM port that the HC-12 has been assigned eg. COM4: "),
				baudrate=9600,
				timeout=0.05)
		else:
			print("What laptop is this running on?")
			quit()

		# If an error is encountered here it will be handled in base_station.py

		# Start handshake procedure
		handshake_complete = False
		print("HC-12 Connected - waiting for message from drone")

		while not handshake_complete:
			# See if a new message is received every 0.5 seconds
			time.sleep(0.5)
			received = self.read_message()

			if received is not None:
				print(received)

			if received == "drone_online":
				# Drone is online so send a response that GCS is too
				epoch_string = str(calendar.timegm(time.localtime()))
				print("Responding: " + "gcs_online&" + epoch_string)
				self.send_message("gcs_online&" + epoch_string)
			elif received == "Handshake complete.":
				# If the handshake is successful this will break the loop
				handshake_complete = True

	def read_message(self):
		"""
		Read the latest message from the serial buffer and return it
		Return None if no message available
		"""
		message_length = self.ser.in_waiting

		if message_length > 0:
			received = self.ser.readline().decode().strip()
		else:
			received = None

		return received

	def send_message(self, to_send):
		"""
		Send message to drone
		"""
		self.ser.write((to_send + "\n").encode('utf-8'))

	def is_comms_open(self):
		"""
		Returns whether the communication link has failed (as verification the drone has shut down)
		"""
		return self.ser.is_open

	def close(self):
		"""
		Close the serial link to the HC-12 module
		"""
		self.ser.close()


########################################
#           MODULE TESTBENCH           #
########################################

if __name__ == "__main__":
	drone = DroneComms()
	counter = 0

	while True:
		message = "Testing" + str(counter).zfill(3)
		drone.send_message(message)
		print("Sent: " + message)

		time.sleep(0.5)
		response = drone.read_message()
		if response is not None:
			print("Received: " + response)
		time.sleep(2)
		counter += 1

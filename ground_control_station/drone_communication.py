# ES410 Autonomous Drone
# Owner: William Gower
# File: ground_communication.py
# Description: Module to handle serial communication to the drone from the GCS

import serial


class DroneComms:
	def __init__(self):
		"""
		start wireless serial connection to drone
		"""
		self.ser = serial.Serial(
			"/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0",
			baudrate=9600)

	def read_message(self):
		"""
		Read the latest message from the serial buffer and return it
		Will - is this going to return None if no message read?
		"""
		return self.ser.readline()

	def send_message(self, message):
		"""
		Send message to drone
		"""
		self.ser.write(message + "\n")

	def is_comms_open(self):
		"""
		Returns whether the communication link has failed (as verification the drone has shut down)
		"""
		return self.ser.is_open

	def close(self):
		"""
		do we need to close this link from the GCS?
		"""
		self.ser.close()

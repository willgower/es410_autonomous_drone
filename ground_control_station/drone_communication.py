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
			baudrate=9600,
			timeout=0)
		if self.ser.is_open:
			print("Seemed to conenct")
		else:
			print("not good")

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
		do we need to close this link from the GCS?
		"""
		self.ser.close()


if __name__ == "__main__":
	import time

	drone = DroneComms()
	counter = 0

	while True:
		message = "Testing" + str(counter).zfill(2)
		drone.send_message(message)
		print("Sent: " + message)

		time.sleep(0.5)
		response = drone.read_message()
		if response is not None:
			print("Received: " + response)
		time.sleep(0.5)
		counter += 1

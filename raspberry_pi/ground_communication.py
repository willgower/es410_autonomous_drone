# ES410 Autonomous Drone
# Owner: William Gower
# File: ground_communication.py
# Description: Module to handle serial communication to the ground control station

import serial


class GroundControlStation:
    def __init__(self):
        """
        Start wireless serial connection to the GCS using the NRF24L01 modules.
        Timeout - 10s
        """

        self.ser = serial.Serial('/dev/ttyS0', 9600, timeout=0)

        if self.ser.is_open:
            self.initSuccessful = True
        else:
            self.initSuccessful = False

    def read_message(self):
        """
        Read the latest message from the serial buffer and return it without:
            - whitespace
            - carriage return
            - new line
        """
        return self.ser.readline().decode().strip()

    def send_message(self, message):
        """
        Send the message back to the GCS
        """
        self.ser.write(message.encode('utf-8'))

    def close(self):
        """
        prepare for system shutdown
        stop processes, close communications and shutdown hardware where possible
        """
        self.ser.close()


if __name__ == "__main__":
    gcs = GroundControlStation()

    while True:
        received = gcs.read_message()

        if received is not None:
            print("Received: " + received)
            gcs.send_message(received + " --- RESPONSE!")
            print("Sent reply")

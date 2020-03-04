# ES410 Autonomous Drone
# Owner: William Gower
# File: ground_communication.py
# Description: Module to handle serial communication to the ground control station

import serial
from gpiozero import LED
import time
import os


class GroundControlStation:
    def __init__(self):
        """
        Start wireless serial connection to the GCS using the HC-12
        Timeout - 10s
        """

        self.ser = serial.Serial('/dev/ttyS0', 9600, timeout=0.1)

        if self.ser.is_open:
            self.initSuccessful = True
        else:
            self.initSuccessful = False

        self.yellow_led = LED(4)
        self.yellow_led.on()

        # Start handshake procedure
        handshake_complete = False

        while not handshake_complete:
            self.ser.write("drone_online\n".encode('utf-8'))
            time.sleep(0.5)

            handshake_response = self.read_message()
            if handshake_response is None:
                continue

            if handshake_response[:10] == "gcs_online":
                epoch_string = handshake_response[11:]
                time_object = time.gmtime(int(epoch_string))
                time_string = time.strftime("%a %b %d %H:%M:%S UTC %Y", time_object)
                try:
                    os.system("sudo date -s \"{}\"".format(time_string))
                except:
                    self.send_message("Error updating time - please try again")
                    continue
                else:
                    self.send_message("RPi time updated as: \"" + time_string + "\"")
                    print("RPi time updated as: \"" + time_string + "\"")
                    self.send_message("Handshake complete.")
                    print("Handshake complete.")
                    self.yellow_led.off()
                    handshake_complete = True

    def read_message(self):
        """
        Read the latest message from the serial buffer and return it without:
            - whitespace
            - carriage return
            - new line
        """
        message_length = self.ser.in_waiting

        if message_length > 0:
            message = self.ser.readline().decode('utf-8').strip()
        else:
            message = None

        return message

    def send_message(self, message):
        """
        Send the message back to the GCS
        """
        self.yellow_led.off()
        self.yellow_led.blink(on_time=0.05, off_time=0.05, n=6)  # Flash quick for 0.5 seconds when sending a message
        self.ser.write((message + "\n").encode('utf-8'))

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
            response = received + " --- RESPONSE!"
            gcs.send_message(response)
            print("Sent reply: " + response)

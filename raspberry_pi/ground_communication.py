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
        # The HC-12 will always be plugged in on the GPIO Rx/Tx pins
        self.ser = serial.Serial('/dev/ttyS0', 9600, timeout=0.1)

        if self.ser.is_open:
            self.initSuccessful = True
        else:
            self.initSuccessful = False

        # Start handshake procedure
        handshake_complete = False
        print("Starting Handshake procedure with GCS")

        # Make the yellow LED go solid while handshake procedure is completing
        self.yellow_led = LED(4)
        self.yellow_led.on()

        while not handshake_complete:
            # Send an 'online' message every 0.5 seconds
            self.ser.write("drone_online\n".encode('utf-8'))
            time.sleep(0.5)

            # Get the response, if any, from the GCS
            handshake_response = self.read_message()
            if handshake_response is None:
                continue

            # If a response was received, see if it is valid and process it
            if handshake_response[:10] == "gcs_online":
                # Extract the time sent from the GCS
                epoch_string = handshake_response[11:]
                time_object = time.gmtime(int(epoch_string))
                time_string = time.strftime("%a %b %d %H:%M:%S UTC %Y", time_object)
                try:
                    # Try to update the system time
                    os.system("sudo date -s \"{}\"".format(time_string))
                except:
                    self.send_message("Error updating time - please try again")
                    continue
                else:
                    # If time update was successful, let the GCS know and finish handshake
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
            try:
                message = self.ser.readline().decode('utf-8').strip()
            except:
                message = None
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


########################################
#           MODULE TESTBENCH           #
########################################

if __name__ == "__main__":
    gcs = GroundControlStation()

    while True:
        received = gcs.read_message()

        if received is not None:
            print("Received: " + received)
            response = received + " --- RESPONSE!"
            gcs.send_message(response)
            print("Sent reply: " + response)

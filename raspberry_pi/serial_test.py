import serial
import time

wireless = serial.Serial('/dev/ttyS0', 9600)

while True:
    wireless.write("hello world!\n".encode('utf-8'))
    print("sent")
    time.sleep(1)

import serial
import time

wireless = serial.Serial('/dev/ttyS0', 9600)

while True:
    wireless.write('hello world!\n')
    print("sent")
    time.sleep(1)

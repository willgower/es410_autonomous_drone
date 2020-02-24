import time
import serial

wireless = serial.Serial(port='/dev/ttyAMA0', baudrate=9600)

counter = 0

while True:
    wireless.write("Does this work?".encode('utf-8'))
    print("sent")

    r = wireless.read(100)

    if r:
        print(r)

    time.sleep(1)

import serial
import sys

ser = serial.Serial('/dev/ttyS0', 9600, timeout=0)

while True:
    x = sys.stdin.readline().strip()
    if len(x) > 0:
        ser.write((x + "\n").encode('utf-8'))

    message_length = ser.in_waiting
    if len(message_length) > 0:
        message = ser.read(message_length).decode()
        print(message)

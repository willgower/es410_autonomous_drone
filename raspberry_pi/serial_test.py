import serial
import sys

ser = serial.Serial('/dev/ttyS0', 9600, timeout=0)

while True:
    x = sys.stdin.readline().strip()
    if len(x) > 0:
        ser.write((x + "\n").encode('utf-8'))

    received_data = ser.read(100).decode()
    if len(received_data) > 0:
        print(received_data)

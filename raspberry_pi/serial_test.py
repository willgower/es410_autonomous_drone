import serial

ser = serial.Serial('/dev/ttyS0', 9600)

while True:
    x = input()
    if len(x) > 0:
        ser.write((x + "\n").encode('utf-8'))

    received_data = ser.read(100).decode()
    if len(received_data) > 0:
        print(received_data)

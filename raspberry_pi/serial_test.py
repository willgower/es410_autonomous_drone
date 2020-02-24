import serial

ser = serial.Serial('/dev/ttyS0', 9600)

while True:
    x = input()
    if len(x) > 0:
        ser.write((x + "\n").encode('utf-8'))

    received_data = ser.readline()  # read serial port
    print(received_data)  # print received data

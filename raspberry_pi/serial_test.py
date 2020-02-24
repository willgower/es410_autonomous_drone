import serial

ser = serial.Serial('/dev/ttyS0', 9600)

while True:
    x = input()
    if len(x) > 0:
        ser.write((x + "\n").encode('utf-8'))

    received_data = ser.read()  # read serial port
    data_left = ser.inWaiting()
    received_data += ser.read(data_left)
    print(received_data)  # print received data

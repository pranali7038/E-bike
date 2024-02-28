import serial
import struct

# Set the correct serial port and baud rate for your Arduino
arduino_port = "/dev/ttyUSB0"  # Change this to your Arduino's serial port
baud_rate = 115200  # Make sure it matches the baud rate used in your Arduino sketch

# Create a serial connection
ser = serial.Serial(arduino_port, baud_rate)

def gps_arduino():
    # Read 4 bytes (32 bits) from Arduino
    data = ser.read(4)

    # Unpack the binary data into a float
    value = struct.unpack('f', data)[0]
    speed = int(value*10)
    return speed

# try:
#     while True:
#         # Read float data from Arduino
#         value = read_float_from_arduino()

#         # Do something with the float value (print it for now)
#         print(round(value,2))

# except KeyboardInterrupt:
#     # Close the serial connection when the program is terminated
#     ser.close()
#     print("Serial connection closed.")
# while(1):
#     print(gps_arduino())
gps_arduino()
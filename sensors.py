import RPi.GPIO as GPIO
import time
import os
import glob

SMOKE_PIN = 17

# These two lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
# Get all the filenames beginning with 28 in the path base_dir. 

device_folder_list = glob.glob(base_dir + '28*')

if not device_folder_list:
    print('Temperature sensor not detected!!')
else:
    device_folder = device_folder_list[0]
    device_file = device_folder + '/w1_slave'

    def read_rom():
        name_file = device_folder + '/name'
        f = open(name_file, 'r')                                                             
        return f.readline()
        
    def read_temp_raw():
        try:
            f = open(device_file, 'r')
            lines = f.readlines()
            f.close()
            return lines
        except FileNotFoundError:
            print('read_temp_raw')
            return None
    
    def read_sensor():
        lines = read_temp_raw()
        analog_sensor = GPIO.input(SMOKE_PIN)

        # Analyze if the last 3 characters are 'YES'.
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
            analog_sensor = GPIO.input(SMOKE_PIN)

        # Find the index of 't=' in a string.
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            # Read the temperature .
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_c = round(temp_c)
            return temp_c, analog_sensor
            
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SMOKE_PIN, GPIO.IN)

    read_sensor()

import RPi.GPIO as GPIO
from dashboard import TriggerAction
from gps import gps_arduino
# from sensors import read_sensor
import time
import random
import threading

GPIO.setmode(GPIO.BCM)

smoke_pin = 17
accelerator_pin = 24
break_pin = 18
horn_pin = 27
indicator1_pin = 22
indicator2_pin = 16
headLight_pin = 5
headLight2_pin = 6


GPIO.setup(accelerator_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(break_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(horn_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(indicator1_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(indicator2_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(smoke_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(headLight_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(headLight2_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

trigger_action = TriggerAction()

# Function to continuously read the accelerator pin
def read_accelerator():
    time.sleep(6)
    while True:
        # speed temp
        if GPIO.input(accelerator_pin) == GPIO.HIGH:
            # temp, smoke = read_sensor()
            temp = random.randint(20, 100)  # replace with actual sensor data
            speed = random.randint(20, 100)  # replace with actual sensor data
            # speed = gps_arduino()
            trigger_action.set_speed(speed, temp)
        elif GPIO.input(accelerator_pin) == GPIO.HIGH:
            trigger_action.release_accelerator()
        time.sleep(0.1)  # adjust delay as needed

        # Break
        if GPIO.input(break_pin) == GPIO.HIGH:
            trigger_action.apply_break()
        else:
            trigger_action.release_break()

        # Indicator1
        if GPIO.input(indicator1_pin) == GPIO.HIGH:
            trigger_action.on_indicator1()
        elif GPIO.input(indicator1_pin) == GPIO.LOW:
            trigger_action.off_indicator1()

        # Indicator2
        if GPIO.input(indicator2_pin) == GPIO.HIGH:
            trigger_action.on_indicator2()
        elif GPIO.input(indicator2_pin) == GPIO.LOW:
            trigger_action.off_indicator2()

        # Smoke
        if GPIO.input(smoke_pin) == GPIO.HIGH:
            trigger_action.apply_accelerator()
        elif GPIO.input(smoke_pin) == GPIO.LOW:
            trigger_action.release_accelerator()

        # Horn
        if GPIO.input(horn_pin) == GPIO.HIGH:
            trigger_action.sound_horn()
        elif GPIO.input(horn_pin) == GPIO.LOW:
            trigger_action.off_horn()

        # HeadLight
        if GPIO.input(headLight_pin) == GPIO.HIGH:
            trigger_action.on_headLight()
        elif GPIO.input(headLight_pin) == GPIO.LOW:
            trigger_action.off_headLight()

        # HeadLight2
        if GPIO.input(headLight2_pin) == GPIO.HIGH:
            trigger_action.on_headLight2()
        elif GPIO.input(headLight2_pin) == GPIO.LOW:
            trigger_action.off_headLight2()

    
# Start a separate thread for reading the accelerator pin
accelerator_thread = threading.Thread(target=read_accelerator)
accelerator_thread.start()

# Add event detection for other GPIO pins (if needed)
# ...

# To show the dashboard (should be called at the end of your code)
trigger_action.launch_dashboard()

# ... (other code)

try:
    # Your main program logic goes here
    while True:
        time.sleep(0.5)  # Adjust the delay as needed

except KeyboardInterrupt:
    # Cleanup GPIO on keyboard interrupt
    GPIO.cleanup()
    print("GPIO cleanup completed.")
# wiring
# S1  ----  GPIO16
# S2  ----  GPIO20
# S3  ----  GPIO21

import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library

global a, b, c
a = 0
b = 0
c = 0


def button_a_callback(channel):
    global a
    a += 1
    print("Button s1 was pushed", a, "times!")


def button_b_callback(channel):
    global b
    b += 1
    print("Button s2 was pushed", b, "times!")


def button_c_callback(channel):
    global c
    c += 1
    print("Button s3 was pushed", c, "times!")


GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
GPIO.setup(16, GPIO.IN)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(20, GPIO.IN)
GPIO.setup(21, GPIO.IN)
GPIO.add_event_detect(16, GPIO.RISING, callback=button_a_callback)
GPIO.add_event_detect(20, GPIO.RISING, callback=button_b_callback)
GPIO.add_event_detect(21, GPIO.RISING, callback=button_c_callback)

message = input("Press enter to quit\n\n")  # Run until someone presses enter

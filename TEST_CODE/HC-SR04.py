# wiring
# Trig  ----  GPIO27
# Echo  ----  GPIO17

# sudo apt install libgpiod2
# pip install adafruit-circuitpython-hcsr04

import time
import board
import adafruit_hcsr04

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D27, echo_pin=board.D17)

while True:
    try:
        print((sonar.distance,))
    except RuntimeError:
        print("Retrying!")
    time.sleep(0.1)
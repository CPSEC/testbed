import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO_IN = 17

GPIO.setup(GPIO_IN, GPIO.OUT)
GPIO.output(GPIO_IN, GPIO.LOW)

if __name__ == "__main__":
    try:
        GPIO.output(GPIO_IN, GPIO.HIGH)
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        GPIO.output(GPIO_IN, GPIO.LOW)
        GPIO.cleanup()

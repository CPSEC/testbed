import time
import RPi.GPIO as GPIO
GPIO_TRIGGER = 27
GPIO_ECHO = 22

class HCSR04:

    def __init__(self, poll_delay=0.01):

        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        # set GPIO Pins
        GPIO_TRIGGER = 27
        GPIO_ECHO = 22

        # set GPIO direction (IN / OUT)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)

        time.sleep(2)
        self.poll_delay = poll_delay
        self.on = True
        self.output = 0

    def update(self):
        while self.on:
            self.poll()
            time.sleep(self.poll_delay)

    def poll(self):
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        self.output = distance

    def run_threaded(self):
        return self.output

    def run(self):
        self.poll()
        return self.output

    def shutdown(self):
        self.on = False
        GPIO.cleanup()


if __name__ == "__main__":
    iter = 0
    p = HCSR04()
    while iter < 100:
        data = p.run()
        print(data)
        time.sleep(0.01)
        iter += 1

import time
import RPi.GPIO as GPIO

# How to call this part?
# V = Vehicle()
# t = template(p1)
# V.add(t, input=['in1', 'in2'], output=['tdata1','tdata2'], threaded=True)
# V.start()



class buzzer:
    def __init__(self, poll_delay=0.01):
        self.on = True
        self.poll_delay = poll_delay
        # initiate your data

        self.BUZZERPIN = 4

        self.SPEED = 1

        # List of tone-names with frequency
        self.TONES = {"c6": 1047,
                 "b5": 988,
                 "a5": 880,
                 "g5": 784,
                 "f5": 698,
                 "e5": 659,
                 "eb5": 622,
                 "d5": 587,
                 "c5": 523,
                 "b4": 494,
                 "a4": 440,
                 "ab4": 415,
                 "g4": 392,
                 "f4": 349,
                 "e4": 330,
                 "d4": 294,
                 "c4": 262}

        self.SONG = [
            ["e5", 16], ["eb5", 16],
            ["e5", 16], ["eb5", 16], ["e5", 16], ["b4", 16], ["d5", 16], ["c5", 16],
            ["a4", 8], ["p", 16], ["c4", 16], ["e4", 16], ["a4", 16],
            ["b4", 8], ["p", 16], ["e4", 16], ["ab4", 16], ["b4", 16],
            ["c5", 8], ["p", 16], ["e4", 16], ["e5", 16], ["eb5", 16],
            ["e5", 16], ["eb5", 16], ["e5", 16], ["b4", 16], ["d5", 16], ["c5", 16],
            ["a4", 8], ["p", 16], ["c4", 16], ["e4", 16], ["a4", 16],
            ["b4", 8], ["p", 16], ["e4", 16], ["c5", 16], ["b4", 16], ["a4", 4]
]

        # Initiate your part here
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUZZERPIN, GPIO.OUT)

    def run(self):
        self.poll()
        # Call in the control loop
        # Works when threaded=False
        # Input is parameters, Return your output

    def shutdown(self):
        self.on = False
        time.sleep(0.2)
        GPIO.output(self.BUZZERPIN, GPIO.HIGH)
        GPIO.cleanup()  # Release resource

    def update(self):
        while self.on:
            self.poll()
            time.sleep(self.poll_delay)
        # your thread
        # Works when threaded=True

    def run_threaded(self):
        pass

    def poll(self):
        p = GPIO.PWM(self.BUZZERPIN, 440)
        p.start(0.5)
        for t in self.SONG:
            duration = (1. / (t[1] * 0.25 * self.SPEED))
            if t[0] == "p":
                   time.sleep(duration)
            else:
                frequency = self.TONES[t[0]]
                p.ChangeFrequency(frequency)
                p.start(0.5)
                time.sleep(duration)
                p.stop()


# test
if __name__ == "__main__":

    B = buzzer()

    while True:
        B.run()

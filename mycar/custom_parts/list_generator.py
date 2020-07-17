import datetime
import time
from random import random


# How to call this part?
# V = Vehicle()
# t = template(p1)
# V.add(t, input=['in1', 'in2'], output=['tdata1','tdata2'], threaded=True)
# V.start()


class LPulse:
    def __init__(self, interval=1, length=23, lst=None, poll_delay=0.01):
        self.on = True
        self.poll_delay = poll_delay
        # optional, parameter
        self.interval = interval
        if lst is None:
            self.lst = [0.3, 0.4, 0.5, 0.6, 0.7]
        else:
            self.lst = lst
        self.index = 0
        # initiate your data
        self.data = 0
        self.recording = True

        # Initiate your part here
        currentTime = datetime.datetime.now()
        currentLength = interval
        self.nextTime = currentTime + datetime.timedelta(seconds=currentLength)
        self.endTime = currentTime + datetime.timedelta(seconds=length)

    def run(self):
        self.poll()
        return self.data, self.recording

        # Call in the control loop
        # Works when threaded=False
        # Input is parameters, Return your output

    def shutdown(self):
        self.on = False
        time.sleep(0.2)
        # Call once before stop the part

    def update(self):
        while self.on:
            self.poll()
            time.sleep(self.poll_delay)
        # your thread
        # Works when threaded=True

    def run_threaded(self, in1, in2):
        pass
        # return self.tdata1, self.tdata2
        # Call in the control loop
        # Works when threaded=True
        # Similar as run function

    def poll(self):
        currentTime = datetime.datetime.now()
        if currentTime > self.endTime:
            self.data = 0
            self.recording = False
            self.on = False
            return
        if currentTime > self.nextTime:
            self.data = self.lst[self.index]
            self.index += 1
            if self.index == len(self.lst):
                self.index = 0
            currentLength = self.interval
            self.nextTime += datetime.timedelta(seconds=currentLength)

        # your actual function of the thread


# test
if __name__ == "__main__":
    iter = 0
    t = LPulse()
    while iter < 80:
        data, recording = t.run()
        print(data, ' ', recording)
        iter += 1
        time.sleep(0.5)

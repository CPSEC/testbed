import datetime
import time


# How to call this part?
# V = Vehicle()
# t = template(p1)
# V.add(t, input=['in1', 'in2'], output=['tdata1','tdata2'], threaded=True)
# V.start()


class Pulse:
    def __init__(self, interval=2, cycle=0.5, length=20, min=0.0, max=1.0, poll_delay=0.01):
        self.on = True
        self.poll_delay = poll_delay
        # optional, parameter
        self.interval = interval
        self.cycle = cycle
        self.min = min
        self.max = max
        # initiate your data
        self.data = self.min
        self.recording = True

        # Initiate your part here
        currentTime = datetime.datetime.now()
        currentLength = interval * (1-cycle)
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
        return self.tdata1, self.tdata2
        # Call in the control loop
        # Works when threaded=True
        # Similar as run function

    def poll(self):
        currentTime = datetime.datetime.now()
        if currentTime > self.endTime:
            self.data = self.min
            self.recording = False
            self.on = False
            return
        if currentTime > self.nextTime:
            if self.data == self.min:
                self.data = self.max
                currentLength = self.interval * self.cycle
                self.nextTime += datetime.timedelta(seconds=currentLength)
            else:
                self.data = self.min
                currentLength = self.interval * (1-self.cycle)
                self.nextTime += datetime.timedelta(seconds=currentLength)

        # your actual function of the thread


# test
if __name__ == "__main__":
    pass

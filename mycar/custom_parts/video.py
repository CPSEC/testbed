import time
import cv2 as cv

# How to call this part?
# V = Vehicle()
# t = template(p1)
# V.add(t, input=['in1', 'in2'], output=['tdata1','tdata2'], threaded=True)
# V.start()


class Video:
    def __init__(self, poll_delay=0.01):
        self.on = True
        self.poll_delay = poll_delay
        # optional, parameter p1
        self.v = cv.VideoCapture(0)
        self.v.set(3, 160)
        self.v.set(4, 120)
        # Initiate your part here

    def run(self):
        img = self.poll()
        return img

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
        ret, img = self.v.read()
        img = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
        return img.tolist()
        # your actual function of the thread


# test
if __name__ == "__main__":
    iter = 0
    t = template()
    while iter < 3:
        tdata1, tdata2 = t.run()
        print(tdata1, tdata2)
        iter += 1
        time.sleep(0.5)

import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle
import time
from pi_camera import PiCamera, CameraDisplay

# How to call this part?
# V = Vehicle()
# t = template(p1)
# V.add(t, input=['in1', 'in2'], output=['tdata1','tdata2'], threaded=True)
# V.start()

class perspective_warp(object):
    def __init__(self, poll_delay=0.01):
        self.on = True
        #self.img = 0
        self.poll_delay = poll_delay

        # Initiate your part here
        self.img_size = (160,120)
        self.src = np.float32([[25, 90],[138, 90],[40, 70],[100, 70]])
        self.dst = np.float32([[37, 90],[122, 90],[40, 0],[110, 0]])

        self.warped = 0
        self.unwarped = 0 
        self.m = 0 
        self.m_inv = 0
    
    def run(self, img):
        self.poll(img)
        return self.warped, self.unwarped, self.m, self.m_inv
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

    def run_threaded(self, img):
        return self.warped, self.unwarped, self.m, self.m_inv
        # Call in the control loop
        # Works when threaded=True
        # Similar as run function

    def poll(self, img):
        # your actual function of the thread
        
        self.m = cv2.getPerspectiveTransform(self.src, self.dst)
        self.m_inv = cv2.getPerspectiveTransform(self.dst, self.src)
        self.warped = cv2.warpPerspective(img, self.m, self.img_size, flags=cv2.INTER_LINEAR)
        self.unwarped = cv2.warpPerspective(self.warped, self.m_inv, (self.warped.shape[1], self.warped.shape[0]), flags=cv2.INTER_LINEAR)  # DEBUG
        
if __name__ == '__main__':

    # read, perspective warp and save a test image
    img = cv2.imread('/home/pi/testbed/mycar/custom_parts/img/testimg.jpg')
    P = perspective_warp()
    warped, unwarped, m, m_inv = P.run(img)
    writeStatus = cv2.imwrite('/home/pi/testbed/mycar/custom_parts/img/warp_testimg.jpg', warped) 
    if writeStatus is True:
        print("Warped image successfully written")
    else:
        print("problem")

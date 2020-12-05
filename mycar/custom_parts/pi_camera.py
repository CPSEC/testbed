import os
import time
import numpy as np
import glob
import cv2
from donkeycar.utils import rgb2gray

class PiCamera(object):
    def __init__(self, image_w=160, image_h=120, image_d=3, framerate=20, vflip=False, hflip=False):
        from picamera.array import PiRGBArray
        from picamera import PiCamera
        
        resolution = (image_w, image_h)
        # initialize the camera and stream
        self.camera = PiCamera() #PiCamera gets resolution (height, width)
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.camera.vflip = vflip
        self.camera.hflip = hflip
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="rgb", use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.on = True
        self.image_d = image_d

        print('PiCamera loaded.. .warming camera')
        time.sleep(2)


    def run(self):
        f = next(self.stream)
        frame = f.array
        self.rawCapture.truncate(0)
        if self.image_d == 1:
            frame = rgb2gray(frame)
        return frame

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            if self.image_d == 1:
                self.frame = rgb2gray(self.frame)

            # if the thread indicator variable is set, stop the thread
            if not self.on:
                break

    def shutdown(self):
        # indicate that the thread should be stopped
        self.on = False
        print('Stopping PiCamera')
        time.sleep(.5)
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()


class CameraDisplay(object):

    def run(self, image):
        cv2.imshow('camera', image)
        cv2.waitKey(1)

    def shutdown(self):
        cv2.destroyAllwindows()

class WarpCameraDisplay(object):

    def run(self, image):
        warped, unwarped, m, m_inv = image
        cv2.imshow('camera', warped)
        cv2.waitKey(1)

    def shutdown(self):
        cv2.destroyAllwindows()


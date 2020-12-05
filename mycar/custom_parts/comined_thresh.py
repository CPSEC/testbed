import time
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle


# How to call this part?
# V = Vehicle()
# t = template(p1)
# V.add(t, input=['in1', 'in2'], output=['tdata1','tdata2'], threaded=True)
# V.start()



class combined_thresh:
    def __init__(self, image, poll_delay=0.01,):
        self.image = image
        self.thresh_min = 0
        self.thresh_max = 0
        self.sobel_kernel = 0
        self.mag_thresh = 0
        self.dir_thresh = 0
        self.channel = 0
        self.hls_thresh = 0
        self.luv_thresh = 0
        self.l_channel = 0
        self.lab_thresh = 0
        self.b_channel = 0
        self.threshholded = 0

        self.hsv = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)#yellow
        self.lowery = np.array([20, 60, 60])
        self.uppery = np.array([38, 174, 250])
        self.masky = cv2.inRange(self.hsv, self.lowery, self.uppery)
    
        self.lowerw = np.array([150, 150, 150])#white
        self.upperw = np.array([255, 255, 255])
        self.maskw= cv2.inRange(self.image, self.lowerw, self.upperw)

    
    def run(self):
        self.poll()
        return self.threshholded
    
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

    def run_threaded(self):
        return self.threshholded
    # Call in the control loop
    # Works when threaded=True
    # Similar as run function
    
    def poll(self):
        # combine all kinds of thresholds
        #abs_sobel_thresh(
        #    img, orient='x', thresh_min=80, thresh_max=255)

        self.thresh_min = 80
        self.thresh_max = 255
        # Convert to grayscale
        gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        # Apply x or y gradient with the OpenCV Sobel() function
        # and take the absolute value
        #if orient == 'x':
        abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 1, 0))
        #if orient == 'y':
        #    abs_sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 0, 1))
        # Rescale back to 8 bit integer
        scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
        # Create a copy and apply the threshold
        binary_output_abs = np.zeros_like(scaled_sobel)
        # Here I'm using inclusive (>=, <=) thresholds, but exclusive is ok too
        binary_output_abs[(scaled_sobel >= self.thresh_min) & (scaled_sobel <= self.thresh_max)] = 1

        # Return the result
        x_threshd = binary_output_abs


        #mag_threshd = mag_thresh(img, sobel_kernel=3, mag_thresh=(80, 255))

        #def mag_thresh(img, sobel_kernel=3, mag_thresh=(0, 255)):

        self.sobel_kernel = 3
        self.mag_thresh = (80,255)

        # Convert to grayscale
        # Take both Sobel x and y gradients
        mag_sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=self.sobel_kernel)
        mag_sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=self.sobel_kernel)
        # Calculate the gradient magnitude
        gradmag = np.sqrt( mag_sobelx**2 +  mag_sobely**2)
        # Rescale to 8 bit
        scale_factor = np.max(gradmag)/255
        gradmag = (gradmag/scale_factor).astype(np.uint8)
        # Create a binary image of ones where threshold is met, zeros otherwise
        binary_output_mag = np.zeros_like(gradmag)
        binary_output_mag[(gradmag >= self.mag_thresh[0]) & (gradmag <= self.mag_thresh[1])] = 1

        # Return the binary image
        mag_threshd = binary_output_mag
        #def dir_threshold(img, sobel_kernel=3, thresh=(0, np.pi/2)):

        #dir_threshd = dir_threshold(img, sobel_kernel=3, thresh=(0.7, 1.3))
        self.dir_thresh = (0.7, 1.3)
        

        # Calculate the x and y gradients
        dir_sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=self.sobel_kernel)
        dir_sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=self.sobel_kernel)
        # Take the absolute value of the gradient direction,
        # apply a threshold, and create a binary image result
        absgraddir = np.arctan2(np.absolute(dir_sobely), np.absolute(dir_sobelx))
        binary_output_dir = np.zeros_like(absgraddir)
        binary_output_dir[(absgraddir >= self.dir_thresh[0]) & (absgraddir <= self.dir_thresh[1])] = 1
        dir_threshd = binary_output_dir

        #hls_threshd = hls_select(img, thresh=(180, 255))

        #def hls_select(img, channel='s', thresh=(0, 255)):
        """
        Filter by s channel of hls color space
        Patameter:
            img:
            channel:
            thresh:
        Return:
        """
        self.channel = 's'
        self.hls_thresh = (0,255)
        hls = cv2.cvtColor(self.image, cv2.COLOR_RGB2HLS)
        if self.channel == 'h':
            self.channel = hls[:, :, 0]
        elif self.channel == 'l':
            self.channel = hls[:, :, 1]
        else:
            self.channel = hls[:, :, 2]
        binary_output_hls = np.zeros_like(self.channel)
        binary_output_hls[(self.channel >  self.hls_thresh[0]) & (self.channel <=  self.hls_thresh[1])] = 1
        hls_threshd = binary_output_hls
   
        # def luv_select(img, thresh=(0, 255)):
        self.luv_thresh=(200, 255)
        luv = cv2.cvtColor(self.image, cv2.COLOR_RGB2LUV)
        self.l_channel = luv[:, :, 0]
        binary_output_luv = np.zeros_like(self.l_channel)
        binary_output_luv[(self.l_channel > self.luv_thresh[0]) & (self.l_channel <= self.luv_thresh[1])] = 1
        luv_threshd= binary_output_luv
        
        # def lab_select(img, thresh=(0, 255)):
        self.lab_thresh=(155, 200)
        lab = cv2.cvtColor(self.image, cv2.COLOR_RGB2Lab)
        self.b_channel = lab[:, :, 2]
        binary_output_lab = np.zeros_like(self.b_channel)
        binary_output_lab[(self.b_channel > self.lab_thresh[0]) & (self.b_channel <= self.lab_thresh[1])] = 1
        lab_threshd = lab_binary_output
        
        # lab_threshd = lab_select(img, thresh=(155, 200))
        # hls_threshd = hls_select(img, thresh=(180, 255))
        
        # lab_threshd = lab_select(img, thresh=(155, 200))       

        # luv_threshd = luv_select(img, thresh=(200, 255))

        # Thresholding combination
        self.threshholded = np.zeros_like(x_threshd)
        # threshholded[((x_threshd == 1) & (mag_threshd == 1)) | ((dir_threshd == 1) & (
        #     hls_threshd == 1)) | (luv_threshd == 1)] = 255
        self.threshholded[((x_threshd == 1) & (mag_threshd == 1) & (self.maskw == 1)) | (luv_threshd == 1) ] = 255


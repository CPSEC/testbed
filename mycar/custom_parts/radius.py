import time
import numpy as np
import matplotlib.image as mpimg
import numpy as np
from cv2 import cv2
import matplotlib.pyplot as plt


# How to call this part?
# V = Vehicle()
# t = template(p1)
# V.add(t, input=['in1', 'in2'], output=['tdata1','tdata2'], threaded=True)
# V.start()



class radius(object):
    def __init__(self, poll_delay=0.01):
        self.on = True
        self.poll_delay = poll_delay
        # initiate your data
        
        self.ym_per_pix = 1/10  # meters per pixel in y dimension
        self.xm_per_pix = 0.45/150  # meters per pixel in x dimension
       
        # print(curvature)
        
        # Initiate your part here
    
    def run(self,binary_warped, right_fit, left_fit):
        self.binary_warped = binary_warped
        self.right_fit = right_fit
        self.left_fit = left_fit
        self.poll()
        return self.curvature, self.distance_from_center
    
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
        pass
    # Call in the control loop
    # Works when threaded=True
    # Similar as run function
    
    def poll(self):
        # Create an image to draw the lines on
        self.binary_warped = np.array(self.binary_warped)
        ploty = np.linspace(0, self.binary_warped.shape[0]-1, self.binary_warped.shape[0])
        leftx = self.left_fit[0]*ploty**2 + self.left_fit[1]*ploty + self.left_fit[2]
        rightx = self.right_fit[0]*ploty**2 + self.right_fit[1]*ploty + self.right_fit[2]
        
        left_fit_cr = np.polyfit(ploty*self.ym_per_pix, leftx*self.xm_per_pix, 2)
        right_fit_cr = np.polyfit(ploty*self.ym_per_pix, rightx*self.xm_per_pix, 2)
        
        #warp_zero = np.zeros_like(self.binary_warped).astype(np.uint8)
        #color_warp = np.dstack((warp_zero, warp_zero, warp_zero))
        # Recast the x and y points into usable format for cv2.fillPoly()
        #pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
        #pts = np.hstack((pts_left, pts_right))
        
        y_eval = np.max(ploty)
        # Fit new polynomials to x,y in world space

        # Calculate the new radii of curvature
        left_curverad = ((1 + (2*left_fit_cr[0]*y_eval*self.ym_per_pix +
                               left_fit_cr[1])**2)**1.5) / np.absolute(2*left_fit_cr[0])
        right_curverad = ((1 + (2*right_fit_cr[0]*y_eval*self.ym_per_pix +
                                right_fit_cr[1])**2)**1.5) / np.absolute(2*right_fit_cr[0])
        self.curvature = ((left_curverad + right_curverad) / 2)
        
        # lane_width = np.absolute(leftx[719] - rightx[719])
        lane_width = np.absolute(leftx[119] - rightx[119])
        lane_xm_per_pix = 0.45 / lane_width
        # veh_pos = (((leftx[719] + rightx[719]) * lane_xm_per_pix) / 2.)
        veh_pos = (((leftx[119] + rightx[119]) * lane_xm_per_pix) / 2.)
        cen_pos = ((self.binary_warped.shape[1] * lane_xm_per_pix) / 2.)
        self.distance_from_center = cen_pos - veh_pos



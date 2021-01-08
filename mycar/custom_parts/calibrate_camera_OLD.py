
import time
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle
import glob
import donkeycar as dk
from pi_camera import PiCamera, CameraDisplay

Cam = PiCamera()
frame = Cam.run()


class calibrate_camera:
    def __init__(self, poll_delay=0.01,):
        self.on = True
        self.poll_delay = poll_delay
        
        # initiate your data
        self.objp_list = []
        self.corners_list = []
        self.mtx = 0
        self.dist = 0
        self.rvecs = 0
        self.tvecs = 0
        
        # Initiate your part here
        self.objp_dict = {
            1: (9, 5),
            2: (9, 6),
            3: (9, 6),
            4: (9, 6),
            5: (9, 6),
            6: (9, 6),
            7: (9, 6),
            8: (9, 6),
            9: (9, 6),
            10: (9, 6),
            11: (9, 6),
            12: (9, 6),
            13: (9, 6),
            14: (9, 6),
            15: (9, 6),
            16: (9, 6),
            17: (9, 6),
            18: (9, 6),
            19: (9, 6),
            20: (9, 6),
            }
    
    def run(self):
        self.poll()
        return self.mtx, self.dist
    
    
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
        return self.mtx, self.dist
    
        # Call in the control loop
        # Works when threaded=True
        # Similar as run function
    
    def poll(self):
        for k in self.objp_dict:
            nx, ny = self.objp_dict[k]
        
            # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
            objp = np.zeros((nx*ny,3), np.float32)
            objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2)

            # Make a list of calibration images
            fname = 'camera_cal/calibration%s.jpg' % str(k)
            img = cv2.imread(fname)
                       # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Find the chessboard corners
            ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
            
            # If found, save & draw corners
            if ret == True:
                # Save object points and corresponding corners
                self.objp_list.append(objp)
                self.corners_list.append(corners)
        
                # Draw and display the corners
                #cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
                #plt.imshow(img)
                #plt.show()
                #print('Found corners for %s' % fname)
            else:
                print('Warning: ret = %s for %s' % (ret, fname))
# your actual function of the thread
        img = cv2.imread('camera_cal/Checkerboard.jpg')
        img_size = (img.shape[1], img.shape[0])
        ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(self.objp_list, self.corners_list, img_size,None,None)


# test
if __name__ == "__main__":
    C = calibrate_camera()
    mtx,dist = C.run()
    save_dict = {'mtx': mtx, 'dist': dist}
    with open('calibrate_camera.p', 'wb') as f:
        pickle.dump(save_dict, f)

    # Undistort example calibration image
    img = mpimg.imread('/home/pi/testbed/mycar/custom_parts/img/testimg.jpg')
    dst = cv2.undistort(img, mtx, dist, None, mtx)
    plt.imshow(dst)
    plt.savefig('/home/pi/testbed/mycar/data/test.png')

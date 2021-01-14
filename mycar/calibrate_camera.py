
import time
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle
import glob
import donkeycar as dk




class calibrate_camera(object):
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
        self.dst = 0
        self.camera = 0
        # Initiate your part here
        self.objp_dict = {
            1: (8, 6),
            2: (8, 6),
            3: (8, 6),
            4: (8, 6),
            5: (8, 6),
            6: (8, 6),
            7: (8, 6),
            8: (8, 6),
            9: (8, 6),
            10: (8, 6),
            11: (8, 6),
            12: (8, 6),
            13: (8, 6),
            14: (8, 6),
            15: (8, 6),
            16: (8, 6),
            17: (8, 6),
            18: (8, 6),
            19: (8, 6),
            20: (8, 6),
            }

           
    
    def run(self):
        #self.camera = camera
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

    def run_threaded(self):
        #self.camera = camera
        return self.mtx, self.dist
    
        # Call in the control loop
        # Works when threaded=True
        # Similar as run function
    
    def poll(self):
    
    #while self.k < 20:
        for k in self.objp_dict:
            nx, ny = self.objp_dict[k]
        
            # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
            objp = np.zeros((nx*ny,3), np.float32)
            objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2)

            # Make a list of calibration images
            fname = '/home/pi/testbed/mycar/data/160120/calibrate%s.jpg' % str(k)
            img = cv2.imread(fname)
            x,y = img.shape[0:2]
            img = cv2.resize(img, (int(y*3), int(x*3)))
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
            
            print(k)
                #self.k += 1

    
        fname = '/home/pi/testbed/mycar/data/160120/calibrate1.jpg'
        img = cv2.imread(fname)
        img_size = (img.shape[1], img.shape[0])
        ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(self.objp_list, self.corners_list, img_size, None, None)
        print('mtx: ', self.mtx)
        print('dist: ', self.dist)


        #self.camera = np.float32(self.camera)
        #self.dst = cv2.undistort(self.camera, self.mtx, self.dist, None, self.mtx)            
            
            
        #img = cv2.imread('/home/pi/testbed/mycar/custom_parts/camera_cal/Checkerboard.jpg')
        #img_size = (img.shape[1], img.shape[0])
        #ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(self.objp_list, self.corners_list, img_size, None, None)
        #self.camera = np.float32(self.camera)
        #self.dst = cv2.undistort(self.camera, self.mtx, self.dist, None, self.mtx)





# test
if __name__ == "__main__":
    C = calibrate_camera()
    mtx,dist = C.run()
    save_dict = {'mtx': mtx, 'dist': dist}
    with open('calibrate_camera.p', 'wb') as f:
        pickle.dump(save_dict, f)

    # Undistort example calibration image
    img = mpimg.imread('/home/pi/testbed/mycar/data/160120/test.jpg')
    x,y = img.shape[0:2]
    img = cv2.resize(img, (int(y*3), int(x*3)))
    dst = cv2.undistort(img, mtx, dist, None, mtx)
    plt.imshow(dst)
    plt.savefig('/home/pi/testbed/mycar/data/test5.png')

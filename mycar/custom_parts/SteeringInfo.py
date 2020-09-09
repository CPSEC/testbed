import time
from line.camera_calibration import *
from line.threasholding import *
from line.perspective_transform import *
from line.detect_lane import *
from line.cal_curv_pos import *
from line.show import *

# How to call this part?
# V = Vehicle()
# t = template(p1)
# V.add(t, input=['in1', 'in2'], output=['tdata1','tdata2'], threaded=True)
# V.start()



class SteeringControl:
    def __init__(self, poll_delay=0.01):
        self.on = True
        self.poll_delay = poll_delay
        # optional, parameter p1
        # initiate your data
        self.curvature = 0
        self.distance_from_center = 0
        # Initiate your part here

    def run(self, data):
        self.poll(data)
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

    def run_threaded(self, in1, in2):
        return self.tdata1, self.tdata2
        # Call in the control loop
        # Works when threaded=True
        # Similar as run function

    def poll(self, data):
        lineDetection(data)
        # your actual function of the thread

    def lineDetection(self, img):

        tmp = combine_threshold(img)

        M, Minv = get_M_Minv()
        tmp = cv2.warpPerspective(tmp, M, tmp.shape[1::-1], flags=cv2.INTER_LINEAR)

        left_fit, right_fit, left_lane_inds, right_lane_inds = find_line(tmp)
        # print(left_fit, right_fit, left_lane_inds, right_lane_inds)

        # undist = undistorted_imgs[0]
        # r = draw_area(undist, tmp, Minv, left_fit, right_fit)

        self.curvature, self.distance_from_center = calculate_curv_and_pos(
            tmp, left_fit, right_fit)
        # r = draw_values(r, curvature, distance_from_center)


# test
if __name__ == "__main__":
    iter = 0
    t = template()
    while iter < 3:
        tdata1, tdata2 = t.run()
        print(tdata1, tdata2)
        iter += 1
        time.sleep(0.5)

import time
import logging
import joblib
import datetime


# How to call this part?
# V = Vehicle()
# t = template(p1)
# V.add(t, input=['in1', 'in2'], output=['tdata1','tdata2'], threaded=True)
# V.start()

class PIDSpeed:
    def __init__(self, pid):
        self.pid = pid
        self.on = True
        # initiate your data
        self.throttle = 0
        self.recording = True

        # currentTime = datetime.datetime.now()
        # currentLength = 5
        # length = 30
        # self.nextTime = currentTime + datetime.timedelta(seconds=currentLength)
        # self.endTime = currentTime + datetime.timedelta(seconds=length)

    def run(self, p, i, d, cse):
        self.p = p
        self.i = i
        self.d = d
        self.cse = cse
        self.poll()
        return self.throttle,self.recording

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
        # currentTime = datetime.datetime.now()
        # if currentTime > self.endTime:
        #     self.data = 0
        #     self.recording = False
        #     self.on = False
        #     return
        # if currentTime > self.nextTime:
        self.throttle = self.pid.run(self.p, self.i, self.d, self.cse)
        logging.info("CurrentSpeedError: %f Speed: %f" % (self.cse, self.throttle))

        # print(self.throttle)

        # your actual function of the thread


class PIDController:
    """ Performs a PID computation and returns a control value.
        This is based on the elapsed time (dt) and the current value of the process variable
        (i.e. the thing we're measuring and trying to change).
        https://github.com/chrisspen/pid_controller/blob/master/pid_controller/pid.py
    """

    def __init__(self, debug=False):

        # initialize gains
        # self.Kp = p
        # self.Ki = i
        # self.Kd = d

        # The value the controller is trying to get the system to achieve.


        # initialize delta t variables
        self.prev_tm = time.time()
        self.prev_err = 0
        self.error = None
        self.totalError = 0

        # initialize the output
        self.alpha = 0

        # debug flag (set to True for console output)
        self.debug = debug

    def run(self, p, i, d, err):
        self.Kp = p
        self.Ki = i
        self.Kd = d
        curr_tm = time.time()

        self.difError = err - self.prev_err

        # Calculate time differential.
        dt = curr_tm - self.prev_tm

        # Initialize output variable.
        curr_alpha = 0

        # Add proportional component.
        curr_alpha += self.Kp * err

        # Add integral component.
        curr_alpha += self.Ki * (self.totalError * dt)

        # Add differential component (avoiding divide-by-zero).
        if dt > 0:
            curr_alpha += self.Kd * ((self.difError) / float(dt))

        # Maintain memory for next loop.
        self.prev_tm = curr_tm
        self.prev_err = err
        self.totalError += err

        # Update the output
        self.alpha = curr_alpha

        if (self.debug):
            print('PID err value:', round(err, 4))
            print('PID output:', round(curr_alpha, 4))

        return curr_alpha


class CSE(object):
    def __init__(self):
        #self.target = target
        pass

    def run(self, target, speed):
        self.target = target
        cse = float(self.target) - speed
        # print(speed)

        return cse


# # test
# if __name__ == "__main__":
#     iter = 0
#     t = RPulse()
#     while iter < 80:
#         data, recording = t.run()
#         print(data, ' ', recording)
#         iter += 1
#         time.sleep(0.5)

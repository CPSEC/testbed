import time
import glpk
import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

# dependency
# pip install setuptools_scm
# pyglpk https://github.com/bradfordboyle/pyglpk
# cd pyglpk
# make
# make install


class Recovery:
    def __init__(self, Ad, Bd, poll_delay=0.01):
        self.on = True
        self.poll_delay = poll_delay

        # prepare lp matrix
        self.Ad = Ad
        self.Bd = Bd
        self.m = self.Ad.shape[0]
        self.n = self.Bd.shape[1]

    def run(self, in1=0, in2=0):
        self.poll()
        return self.tdata1, self.tdata2

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

    def poll(self, k, initial_set_lo, initial_set_up, target_set_lo, target_set_up, safe_set_lo, safe_set_up,
             control_lo, control_up, debug=True):

        start = time.time()

        # ---------------prepare matrix
        row_num = self.m * k
        col_num = (k+1)*self.m + self.n*k
        matrix = np.zeros((row_num, col_num), np.float)
        # fill Ad
        for i in range(0, self.m*k, self.m):
            matrix[i:i+self.m, i:i+self.m] = -self.Ad
        # fill 1
        for i in range(0, self.m*k):
            matrix[i, i+self.m] = 1
        # fill Bd
        for i in range(0, k):
            x = i * self.m
            y = self.m*(k+1)+self.n*i
            matrix[x:x+self.m, y:y+self.n] = -self.Bd

        # ---------------- def problem
        lp = glpk.LPX()
        lp.name = 'recovery'
        lp.obj.maximize = False

        # ---------------- rows
        lp.rows.add(row_num)
        for r in lp.rows:
            r.bounds = 0

        # ---------------- cols
        lp.cols.add(col_num)
        lp.obj[:] = [1] * col_num
        # initial set bound
        for i in range(self.m):
            lp.cols[i].bounds = initial_set_lo[i], initial_set_up[i]
        # safe set bound
        for i in range(1, k):
            for j in range(self.m):
                lp.cols[i*self.m+j].bounds = safe_set_lo[j], safe_set_up[j]
        # target set bound
        for i in range(self.m):
            lp.cols[self.m*k+i].bounds = target_set_lo[i], target_set_up[i]
        # control bound
        for i in range(k):
            for j in range(self.n):
                lp.cols[self.m*(k+1)+i*self.n+j].bounds = control_lo[j], control_up[j]

        # -----------------  load matrix
        lp.matrix = matrix.flatten().tolist()

        # -----------------  solve problem
        solve_start = time.time()
        lp.simplex()
        if debug:
            end = time.time()
            solve = end - solve_start
            total = end - start
            print('Solve=', solve, 'seconds; ', 'Total=', total, 'seconds.')

        # print state for debug
            state_lst = [r.primal for r in lp.cols[:self.m*(k+1)]]
            state = np.array(state_lst).reshape((k+1, -1))
            print(state.T)

        # return n x k control input
        control_lst = [r.primal for r in lp.cols[self.m*(k+1):]]
        control = np.array(control_lst).reshape((k, -1))
        if debug:
            print(control.T)
        return control.T


# test
if __name__ == "__main__":
    iter = 0
    Ad = np.array([[0.818727296278566, 0.017757312092950], [-3.551462418590050e-04, 0.960785793022168]])
    Bd = np.array([[3.695886905026150e-04], [0.039210511090927]])
    initial_set_lo = [7.999902067622, 79.998780693465]
    initial_set_up = [7.999902067622887, 79.998780693465960]
    target_set_lo = [3.9, -100]
    target_set_up = [4.1, 100]
    safe_set_lo = [1, -150]
    safe_set_up = [8, 150]
    control_lo = [-150]
    control_up = [150]
    t = Recovery(Ad, Bd)
    t.poll(10, initial_set_lo, initial_set_up, target_set_lo, target_set_up, safe_set_lo, safe_set_up, control_lo,
               control_up)
    pass



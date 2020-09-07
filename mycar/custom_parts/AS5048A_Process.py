import multiprocessing
import time
from .AS5048A import AS5048A

shared_mem_size = 400


def feed_position(b1p, b1t, b2p, b2t, b1n, b2n, cbn):
    bp = b1p
    bt = b1t
    bn = b1n
    as5048a = AS5048A()
    idx = 0
    lb = -1
    while True:
        if cbn.value != lb:
            # switch buffer
            idx = 0
            if cbn.value == 1:
                bp = b1p
                bt = b1t
                bn = b1n
            else:
                bp = b2p
                bt = b2t
                bn = b2n
        lb = cbn.value

        # avoid overflow
        if idx > shared_mem_size-1:
            print('share memory is not enough')
            continue

        bp[idx] = as5048a.get_angle(debug=False)
        bt[idx] = time.time_ns()
        # print('current_buff=', cbn.value, '  idx=', bn.value, ' angle=', bp[idx])
        idx += 1
        bn.value = idx
        time.sleep(0.0001)


class speed:

    def __init__(self):
        self.on = True

        # create shared memory
        self.buff1_position = multiprocessing.Array('i', shared_mem_size)
        self.buff1_time = multiprocessing.Array('i', shared_mem_size)
        self.buff1_num = multiprocessing.Value('i')
        self.buff2_position = multiprocessing.Array('i', shared_mem_size)
        self.buff2_time = multiprocessing.Array('i', shared_mem_size)
        self.buff2_num = multiprocessing.Value('i')
        self.current_buff = multiprocessing.Value('i')
        self.current_buff.value = 1

        # create process
        p = multiprocessing.Process(target=feed_position, args=(self.buff1_position, self.buff1_time,
                                                                self.buff2_position, self.buff2_time,
                                                                self.buff1_num, self.buff2_num, self.current_buff))
        p.daemon = True
        p.start()

    def run(self):
        # inform the subprocess change buffer
        last_buff = self.current_buff.value
        if last_buff == 1:
            self.current_buff.value = 2
            bp = self.buff1_position
            bt = self.buff1_time
            bn = self.buff1_num.value
        else:
            self.current_buff.value = 1
            bp = self.buff2_position
            bt = self.buff2_time
            bn = self.buff2_num.value

        p = bp[:bn]
        t = bt[:bn]

        theta_p = []
        theta_t = []
        for i in range(bn - 1):
            theta_t_i = t[i + 1] - t[i]
            # remove tasks missing deadline 1.5ms
            if theta_t_i > 1500000 or theta_t_i < 0:
                continue
            theta_p_i = p[i] - p[i + 1]
            # remove theta p over zero
            if theta_p_i < -10467 or theta_p_i > 10467:
                continue

            theta_t.append(theta_t_i)
            theta_p.append(theta_p_i)

        sum_theta_t = sum(theta_t)
        if sum_theta_t == 0:
            sum_theta_t = 1
        result = (sum(theta_p) / 0x4000) / (sum_theta_t / 1000000000)

        return result

    def shutdown(self):
        self.on = False
        time.sleep(0.2)
        # Call once before stop the part

    def update(self):
        pass

    def run_threaded(self, in1, in2):
        pass

    def poll(self):
        pass
        # your actual function of the thread


# test
if __name__ == "__main__":
    pass

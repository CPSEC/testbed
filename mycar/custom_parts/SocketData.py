#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from math import sin
import socket
import json
import select
from datetime import datetime, timedelta
import time

# How to call this part?
# V = Vehicle()
# t = template(p1)
# V.add(t, input=['in1', 'in2'], output=['tdata1','tdata2'], threaded=True)
# V.start()


class SocketData():
    """
     Do NOT run as thread
    """

    def __init__(self, inputs, poll_delay=1.1):
        self.on = True
        self.poll_delay = poll_delay
        self.index = 0
        self.HOST = '192.168.1.3'
        self.PORT = 13244
        self.inputs = inputs
        self.row = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))
        self.sock.setblocking(False)

        self.rspeed = 0
        self.mp = 0
        self.mi = 0
        self.md = 0

    def run(self, *args):
        pass

    def poll(self):
        cur = datetime.now()
        nxt = cur + timedelta(microseconds=50)
        count = 0
        sep = '\x1e'

        header = ['milliseconds', 'as5048a', 'throttle', 'vm', 'angle', 'bias', 'radius', 'hcsr04', 'vp', 'heading',
                  'roll',
                  'pitch', 'ori_x', 'ori_y', 'ori_z', 'ori_w', 'temp_c', 'mag_x', 'mag_y', 'mag_z', 'gyr_x', 'gyr_y',
                  'gyr_z',
                  'acc_x', 'acc_y', 'acc_z', 'lacc_x', 'lacc_y', 'lacc_z', 'gra_x', 'gra_y', 'gra_z']
        read_sockets, write_sockets, error_sockets = select.select(
            [self.sock], [self.sock], [], 0)

        for s in read_sockets:
            data = s.recv(1024)
            if data:
                df, ignored, buffer = data.decode().partition(sep)

                df_json = json.loads(df)
                self.rspeed = df_json['speed']
                self.mp = df_json['throttle-PID']['P']
                self.mi = df_json['throttle-PID']['I']
                self.md = df_json['throttle-PID']['D']
                # self.sp = df_json['servo-PID']['P']
                # self.si = df_json['servo-PID']['I']
                # self.sd = df_json['servo-PID']['D']
                print('Receive:', data.decode())
                print('------------')

        for s in write_sockets:
            # cur = datetime.now()
            # if cur >= nxt:
            #     # data
            #     d[0] = 0.01 * count
            #     d[1] = 30 * sin(0.1 * count) + 30
            p_dict = {'rspeed': 40,
                      'mp': 0.001748, 'mi': 0.00050, 'md': -0.00000005,
                      'sp': 6, 'si': 7, 'sd': 8}
            d_dict = {'sensor': dict(zip(header, self.row)), 'parameter': p_dict}

            message = (json.dumps(d_dict) + sep).encode()
            self.sock.send(message)
            # print('send', d_dict)

            # nxt = nxt + timedelta(milliseconds=10)
            # count += 1

        # sock.close()
        return self.rspeed, self.mp, self.mi, self.md

    def update(self):
        while self.on:
            self.poll()
            time.sleep(self.poll_delay)

    def run_threaded(self, *args):
        assert len(self.inputs) == len(args)
        current_time = time.time()
        self.row.append(current_time)
        self.row.extend(list(args))


# test
if __name__ == "__main__":
    inputs = [1596765960.2403817, 0.0, 0.2117611089733787, 10.718304, 0.0, None, None, 0, 10.750271999999999, 26.0625,
              1.0625, -0.6875, 0.00372314453125, -0.01092529296875, -0.2255859375, 0.97418212890625, 25, -8.1875,
              15.5625, -43.5, -0.0044444444444444444, -0.0022222222222222222, 0.0, 0.2, 0.12, 9.72, 0.0, 0.01, -0.07,
              0.19, 0.12, 9.8]
    t = SocketData(inputs)
    iter = 0
    while iter < 80:
        t.poll()
        iter += 1

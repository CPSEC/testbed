# dependency:

import time
import socket
import select
import json
import queue

class SocketData:
    def __init__(self, host, port, sensor, parameter, setting, sep, image=False):
        """
        Args:
            host: server ip
            port: server port
            sensor: names of sensor data to be sent
            parameter: names of parameter data to be sent
            setting: get from server, subset of parameter
            sep: to separate two json
            image:  video frame
        """
        self.on = True
        # optional, parameter p1
        self.host = host
        self.port = port
        self.sep = sep
        # initiate your data
        self.sensor_h = sensor
        self.parameter_h = parameter
        self.has_image = image
        self.setting_h = setting
        # Initiate your part here
        self.sock = None
        # get from server
        self.setting = {}
        self.setting_updated = False
        # data to be sent
        self.sensor_queue = queue.Queue()
        self.sensor = {}
        self.parameter = {}
        self.image = None

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.host, self.port))
            sock.setblocking(False)
        except:
            pass
        return sock

    def run(self, in1=0, in2=0):
        pass
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
        # your thread
        # Works when threaded=True

    def run_threaded(self, *args, **kwargs):
        print(kwargs)
        # prepare data to be sent
        for i in kwargs:
            if i in self.sensor_h:
                self.sensor[i] = kwargs[i]
            if i in self.parameter_h:
                self.parameter[i] = kwargs[i]
            if i == 'image':
                self.image = kwargs[i]
        self.sensor_queue.put_nowait(self.sensor)
        # return received data
        setting_lst = []
        if self.setting_updated:
            self.setting_updated = False
            for i in self.setting_h:
                setting_lst.append(self.setting[i])
        else:
            # do not change
            for i in self.setting_h:
                setting_lst.append(kwargs[i])

        return setting_lst
        # Call in the control loop
        # Works when threaded=True
        # Similar as run function

    def poll(self):
        read_sockets, write_sockets, error_sockets = select.select(
            [self.sock], [self.sock], [], 0)

        for s in read_sockets:
            data = s.recv(1024)
            if data:
                try:
                    df, ignored, buffer = data.decode().partition(self.sep)
                    df_json = json.loads(df)
                    self.setting['rspeed'] = df_json['speed']
                    self.setting['mp'] = df_json['throttle-PID']['P']
                    self.setting['mi'] = df_json['throttle-PID']['I']
                    self.setting['md'] = df_json['throttle-PID']['D']
                    self.setting['sp'] = df_json['servo-PID']['P']
                    self.setting['si'] = df_json['servo-PID']['I']
                    self.setting['sd'] = df_json['servo-PID']['D']
                    # TODO: Other setting
                    self.setting_updated = True
                except:
                    pass

        for s in write_sockets:
            if not self.sensor_queue.empty():
                sensor_dict = self.sensor_queue.get_nowait()
                d_dict = {'sensor': sensor_dict}
                if self.parameter:
                    d_dict['parameter'] = self.parameter
                if self.image:
                    d_dict['image'] = self.image

                message = (json.dumps(d_dict) + self.sep).encode()
                while message:
                    try:
                        sent = s.send(message)
                    except BlockingIOError:
                        pass
                    else:
                        message = message[sent:]


# test
if __name__ == "__main__":
    pass

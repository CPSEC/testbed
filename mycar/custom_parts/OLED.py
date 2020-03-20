# config oled service first
from multiprocessing.connection import Client
import pickle
import time


class OLED:

    def __init__(self, OLED_KEY='', OLED_PORT=0, poll_delay=0.1):
        self.authkey = OLED_KEY
        self.port = OLED_PORT
        self.poll_delay = poll_delay
        self.on = True

        self.last_recording = False
        self.recording = False

    def update(self):
        while self.on:
            self.poll(self.recording)
            time.sleep(self.poll_delay)

    def poll(self, recording):
        if recording != self.last_recording:
            self.last_recording = recording
            if recording:
                self.oprint('Start recording.')
            else:
                self.oprint('Stop recording.')

    def run_threaded(self, recording):
        self.recording = recording

    def run(self, recording):
        self.poll(recording)

    def shutdown(self):
        self.on = False

    def send_data(self, icons=None, texts=None):
        address = ('localhost', self.port)
        conn = Client(address, authkey=bytes(self.authkey, 'ascii'))
        data = {}
        if icons:
            data['icons'] = icons
        if texts:
            data['texts'] = texts
        data_str = pickle.dumps(data)
        conn.send(data_str)
        conn.close()

    def oprint(self, output=''):
        self.send_data(texts=[output])


if __name__ == "__main__":
    iter = 0
    p = OLED()
    while iter < 100:
        p.run(True)
        time.sleep(0.01)
        iter += 1
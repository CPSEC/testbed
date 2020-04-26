import time
import os
import datetime
import csv


# How to call this part?
# V = Vehicle()
# t = template(p1)
# V.add(t, input=['in1', 'in2'], output=['tdata1','tdata2'], threaded=True)
# V.start()


class CSVDATA():
    """
     Do NOT run as thread
    """

    def __init__(self, path, inputs, poll_delay=0.01):
        self.on = True
        self.poll_delay = poll_delay
        self.inputs = inputs
        self.index = 0

        self.path = os.path.expanduser(path)
        exists = os.path.exists(self.path)
        if not exists:
            os.makedirs(self.path)

        self.last_time = 0
        self.filepath = ''

    def newfile(self):
        self.index = 0
        filenames = next(os.walk(self.path))[2]
        nums = [int(filename.split('_')[1]) for filename in filenames]
        max_num = max(nums + [0]) + 1
        filename = 'data_' + str(max_num) + '_' + datetime.datetime.now().strftime("%Y%m%d%-H%M%S") + '.csv'
        self.filepath = os.path.join(self.path, filename)

        with open(self.filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header = ['index', 'milliseconds'] + self.inputs
            writer.writerow(header)

    def test(self):
        pass

    def run(self, *args):
        assert len(self.inputs) == len(args)
        current_time = time.time()
        if current_time - self.last_time > 1:
            self.newfile()
        self.poll(current_time, args)
        self.last_time = current_time
        # Call in the control loop
        # Works when threaded=False
        # Input is parameters, Return your output

    def poll(self, current_time, args):
        with open(self.filepath, 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile)
            row = []
            self.index += 1
            row.append(self.index)
            row.append(current_time)
            row.extend(list(args))
            writer.writerow(row)


# test
if __name__ == "__main__":
    path = '~/Code/testbed/mycar/data'
    inputs = ['test1', 'test2', 'test3']
    iter = 0
    t = CSVDATA(path, inputs)
    while iter < 3:
        t.run(1, 2, 3)
        iter += 1
        time.sleep(0.5)
    time.sleep(1)
    iter = 0
    while iter < 3:
        t.run(4, 5, 6)
        iter += 1
        time.sleep(0.5)

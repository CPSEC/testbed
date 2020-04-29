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

    def __init__(self, path, inputs, poll_delay=1.1):
        self.on = True
        self.poll_delay = poll_delay
        self.inputs = inputs
        self.index = 0

        self.path = os.path.expanduser(path)
        exists = os.path.exists(self.path)
        if not exists:
            os.makedirs(self.path)

        self.filepath = ''
        self.createfile = True
        self.buff1 = []
        self.buff2 = []
        self.currentbuff = self.buff1
        self.lastbuff = self.buff2

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
            csvfile.flush()

    def run(self, *args):
        pass

    def taketurn(self, buff):
        if buff == self.buff1:
            return self.buff2
        else:
            return self.buff1

    def poll(self):
        # buffer take turn
        self.lastbuff = self.currentbuff
        self.currentbuff = self.taketurn(self.currentbuff)

        if len(self.lastbuff) == 0:
            # if detect pause, create new file
            self.createfile = True
        else:
            if self.createfile == True:
                self.newfile()
                self.createfile = False
            with open(self.filepath, 'a+', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(self.lastbuff)
                csvfile.flush()
            self.lastbuff.clear()

    def update(self):
        while self.on:
            self.poll()
            time.sleep(self.poll_delay)

    def run_threaded(self, *args):
        assert len(self.inputs) == len(args)
        current_time = time.time()
        row = []
        self.index += 1
        row.append(self.index)
        row.append(current_time)
        row.extend(list(args))
        self.currentbuff.append(row)


# test
if __name__ == "__main__":
    path = '~/Code/testbed/mycar/data'
    inputs = ['test1', 'test2', 'test3']
    iter = 0
    t = CSVDATA(path, inputs)
    while iter < 3:
        t.run_threaded(1,2,3)
        iter += 1
    print(t.currentbuff == t.buff1)
    t.poll()
    while iter < 6:
        t.run_threaded(4,5,6)
        iter += 1
    print(t.currentbuff == t.buff1)
    t.poll()
    while iter < 9:
        t.run_threaded(7,8,9)
        iter += 1
    print(t.currentbuff == t.buff1)
    t.poll()
    print(t.currentbuff == t.buff1)


    t.poll()
    print(t.currentbuff == t.buff1)
    t.poll()
    while iter < 12:
        t.run_threaded(1, 2, 3)
        iter += 1
    print(t.currentbuff == t.buff1)
    t.poll()
    while iter < 15:
        t.run_threaded(4, 5, 6)
        iter += 1
    print(t.currentbuff == t.buff1)
    t.poll()
    while iter < 18:
        t.run_threaded(7, 8, 9)
        iter += 1
    print(t.currentbuff == t.buff1)
    t.poll()

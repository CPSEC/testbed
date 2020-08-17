import time


class Clock:
    def __init__(self):
        self.on = True
        # Initiate your part here

    def run(self):
        return time.time()
        # Call in the control loop
        # Works when threaded=False
        # Input is parameters, Return your output

    def shutdown(self):
        self.on = False
        time.sleep(0.2)


# test
if __name__ == "__main__":
    pass

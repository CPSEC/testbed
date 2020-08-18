import time


class PID:
    def __init__(self, p, i, d, dt, control_up, control_lo):
        self.on = True
        # optional, parameter p1
        self.p = p
        self.i = i
        self.d = d
        self.dt = dt
        self.c_up = control_up
        self.c_lo = control_lo
        # initiate your data
        self.int_error = 0
        self.pre_error = 0
        # Initiate your part here

    def run(self, set_point, measurement, p=None, i=None, d=None):
        # needed when turning
        if p:
            self.p = p
        if i:
            self.i = i
        if d:
            self.d = d

        # error
        error = set_point - measurement

        # integration
        self.int_error += error * self.dt
        iterm = self.int_error * self.i
        # integration anti-windup
        iterm = self.clamp(iterm)

        # differentiation
        diff = (error - self.pre_error) / self.dt
        dterm = diff * self.d

        # proportion
        pterm = error * self.p

        control = pterm + iterm + dterm
        control = self.clamp(control)

        # save state
        self.pre_error = error

        return control

    def clamp(self, value):
        if value < self.c_lo:
            return self.c_lo
        if value > self.c_up:
            return self.c_up
        return value

    def shutdown(self):
        self.on = False
        time.sleep(0.2)
        # Call once before stop the part


# test
if __name__ == "__main__":
    pass

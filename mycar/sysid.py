from donkeycar.vehicle import Vehicle
import donkeycar as dk
from donkeycar.parts.actuator import PCA9685, PWMSteering, PWMThrottle

from custom_parts.ADS1115 import ADS1115
from custom_parts.AS5048A_Process import speed
from custom_parts.SocketData import SocketData
from custom_parts.Clock import Clock
# from custom_parts.PID import PID
from custom_parts.list_generator import LPulse
from custom_parts.PID_new import PID

cfg = dk.load_config()
V = Vehicle()

sensor = ['as5048a', 'throttle', 'vm', 'vp']
parameter = ['rspeed', 'mp', 'mi', 'md', 'sp', 'si', 'sd']
setting = ['rspeed', 'mp', 'mi', 'md', 'sp', 'si', 'sd']


# time of current control step
clock = Clock()
V.add(clock, outputs=['milliseconds'])

# speed sensor
as5048a = speed()
V.add(as5048a, outputs=['as5048a'])

ads1115 = ADS1115(coeff_m=cfg.VM_COEFFICIENT, coeff_p=cfg.VP_COEFFICIENT)
V.add(ads1115, outputs=['vm', 'vp'], threaded=True)

signal_lst = [0.2] #[0] + ([0.22]*3 + [0]*2)*2  + [0.16, 0.18, 0.2, 0.22, 0.24, 0.26, 0.24, 0.22, 0.2, 0.18, 0.16] + [0]
control_input = LPulse(interval=2, length=200, lst=signal_lst)
V.add(control_input, outputs=['throttle', 'recording'])

# actuator - Motor
throttle_controller = PCA9685(cfg.THROTTLE_CHANNEL, cfg.PCA9685_I2C_ADDR, busnum=cfg.PCA9685_I2C_BUSNUM)
throttle = PWMThrottle(controller=throttle_controller,
                       max_pulse=cfg.THROTTLE_FORWARD_PWM,
                       zero_pulse=cfg.THROTTLE_STOPPED_PWM,
                       min_pulse=cfg.THROTTLE_REVERSE_PWM)
V.add(throttle, inputs=['throttle'])

# send data
host = cfg.HOST
port = cfg.PORT
sep = cfg.SEP
inputs = ['milliseconds'] + sensor + parameter
outputs = setting
sock = SocketData(host, port, sensor, parameter, setting, sep)
V.add(sock, inputs=inputs, outputs=outputs, threaded=True)

V.start(rate_hz=cfg.DRIVE_LOOP_HZ,
        max_loop_count=cfg.MAX_LOOPS)

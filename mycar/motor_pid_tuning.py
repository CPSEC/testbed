from donkeycar.vehicle import Vehicle
import donkeycar as dk
from donkeycar.parts.actuator import PCA9685, PWMSteering, PWMThrottle
from custom_parts.AS5048A_Process import speed
from custom_parts.SocketData import SocketData
from custom_parts.Clock import Clock
from custom_parts.PID import PID
from custom_parts.pulse_generator import Pulse

cfg = dk.load_config()
V = Vehicle()

sensor = ['as5048a', 'throttle', 'rspeed']
parameter = ['rspeed', 'mp', 'mi', 'md', 'sp', 'si', 'sd']
setting = ['rspeed', 'mp', 'mi', 'md', 'sp', 'si', 'sd']
V.mem.put(parameter, [40, cfg.MOTOR_P, cfg.MOTOR_I, cfg.MOTOR_D, cfg.SERVO_P, cfg.SERVO_I, cfg.SERVO_D])
# V.mem.put(['throttle'], 0.2)

# time of current control step
clock = Clock()
V.add(clock, outputs=['milliseconds'])

# speed sensor
as5048a = speed()
V.add(as5048a, outputs=['as5048a'])

# reference speed (set point)
pulse = Pulse(interval=10, cycle=0.5, length=300, min=60, max=100)
V.add(pulse, outputs=['rspeed', 'recording'])

# pid controller
p = cfg.MOTOR_P
i = cfg.MOTOR_I
d = cfg.MOTOR_D
dt = 1/cfg.DRIVE_LOOP_HZ
control_up = 1
control_lo = 0
motor_pid = PID(p, i, d, dt, control_up, control_lo)
V.add(motor_pid, inputs=['rspeed', 'as5048a', 'mp', 'mi', 'md'], outputs=['throttle'])

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




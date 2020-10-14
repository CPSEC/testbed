import donkeycar as dk
from custom_parts.Clock import Clock
from custom_parts.AS5048A_Process import speed
from custom_parts.SocketData import SocketData
from donkeycar.parts.camera import PiCamera

cfg = dk.load_config()
V = dk.vehicle.Vehicle()

sensor = ['as5048a', 'throttle', 'rspeed']
parameter = ['rspeed', 'mp', 'mi', 'md', 'sp', 'si', 'sd']
setting = ['rspeed', 'mp', 'mi', 'md', 'sp', 'si', 'sd']
V.mem.put(parameter, [40, cfg.MOTOR_P, cfg.MOTOR_I, cfg.MOTOR_D, cfg.SERVO_P, cfg.SERVO_I, cfg.SERVO_D])

# time of current control step
clock = Clock()
V.add(clock, outputs=['milliseconds'])


# speed sensor
as5048a = speed()
V.add(as5048a, outputs=['as5048a'])

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




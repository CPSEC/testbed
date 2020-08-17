from donkeycar.vehicle import Vehicle
import donkeycar as dk
from custom_parts.AS5048A_Process import speed
from custom_parts.SocketData import SocketData
from custom_parts.Clock import Clock

cfg = dk.load_config()
V = Vehicle()

sensor = ['as5048a']
parameter = ['rspeed', 'mp', 'mi', 'md', 'sp', 'si', 'sd']
setting = ['rspeed', 'mp', 'mi', 'md', 'sp', 'si', 'sd']
V.mem.put(parameter, [40, cfg.MOTOR_P, cfg.MOTOR_I, cfg.MOTOR_D, cfg.SERVO_P, cfg.SERVO_I, cfg.SERVO_D])

clock = Clock()
V.add(clock, outputs=['milliseconds'])

as5048a = speed()
V.add(as5048a, outputs=['as5048a'])

# def __init__(self, host, port, sensor, parameter, setting, sep, image=False, poll_delay=0.01):
host = cfg.HOST
port = cfg.PORT
sep = cfg.SEP
inputs = ['milliseconds'] + sensor + parameter
outputs = setting
sock = SocketData(host, port, sensor, parameter, setting, sep)
V.add(sock, inputs=inputs, outputs=outputs, threaded=True)


V.start(rate_hz=cfg.DRIVE_LOOP_HZ,
        max_loop_count=cfg.MAX_LOOPS)




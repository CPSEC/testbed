from donkeycar.vehicle import Vehicle
import donkeycar as dk
from custom_parts.AS5048A_Process import speed
from custom_parts.SocketData import SocketData

cfg = dk.load_config()
V = Vehicle()

sensor = ['as5048a']
parameter = ['rspeed', 'mp', 'mi', 'md', 'sp', 'si', 'sd']
setting = ['rspeed', 'mp', 'mi', 'md', 'sp', 'si', 'sd']

V.mem.put(parameter, [40, cfg.Motor_P, cfg.Motor_I, cfg.Motor_D, cfg.Servo_P, cfg.Servo_I, cfg.Servo_D])

as5048a = speed()
V.add(as5048a, outputs=['as5048a'])

# def __init__(self, host, port, sensor, parameter, setting, sep, image=False, poll_delay=0.01):
host = cfg.host
port = cfg.port
sep = cfg.sep
inputs = sensor + parameter
outputs = setting
sock = SocketData(host, port, sensor, parameter, setting, sep)
V.add(sock, inputs=inputs, outputs=outputs, threaded=True)


V.start(rate_hz=cfg.DRIVE_LOOP_HZ,
        max_loop_count=cfg.MAX_LOOPS)




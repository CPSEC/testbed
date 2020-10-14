import donkeycar as dk
from custom_parts.Clock import Clock
from custom_parts.AS5048A_Process import speed
from custom_parts.SocketData import SocketData
from custom_parts.video import Video
from custom_parts.BNO055 import BNO055
from donkeycar.parts.camera import PiCamera

cfg = dk.load_config()
V = dk.vehicle.Vehicle()

bno055_output = ["heading", "roll", "pitch", "sys", "gyro", "accel",
                 "mag", "ori_x", "ori_y", "ori_z", "ori_w", "temp_c",
                 "mag_x", "mag_y", "mag_z", "gyr_x", "gyr_y", "gyr_z",
                 "acc_x", "acc_y", "acc_z", "lacc_x", "lacc_y",
                 "lacc_z", "gra_x", "gra_y", "gra_z"]
sensor = ['as5048a', 'throttle', 'rspeed'] + bno055_output
parameter = ['rspeed', 'mp', 'mi', 'md', 'sp', 'si', 'sd']
setting = ['rspeed', 'mp', 'mi', 'md', 'sp', 'si', 'sd']
V.mem.put(parameter, [40, cfg.MOTOR_P, cfg.MOTOR_I, cfg.MOTOR_D, cfg.SERVO_P, cfg.SERVO_I, cfg.SERVO_D])

# time of current control step
clock = Clock()
V.add(clock, outputs=['milliseconds'])


# speed sensor
as5048a = speed()
V.add(as5048a, outputs=['as5048a'])

# bno055
bno055 = BNO055()
V.add(bno055, outputs=bno055_output)

# video
video = Video()
V.add(video, outputs=['image'])

# send data
host = cfg.HOST
port = cfg.PORT
sep = cfg.SEP
inputs = ['milliseconds'] + sensor + parameter + ['image']
outputs = setting
sock = SocketData(host, port, sensor, parameter, setting, sep, image=True)
V.add(sock, inputs=inputs, outputs=outputs, threaded=True)

V.start(rate_hz=cfg.DRIVE_LOOP_HZ,
        max_loop_count=cfg.MAX_LOOPS)




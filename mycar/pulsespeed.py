from donkeycar.vehicle import Vehicle
from donkeycar.parts.datastore import TubHandler
from donkeycar.parts.controller import get_js_controller
from donkeycar.parts.throttle_filter import ThrottleFilter
from donkeycar.parts.actuator import PCA9685, PWMSteering, PWMThrottle
from donkeycar.parts.camera import PiCamera

from custom_parts.HCSR04 import HCSR04
from custom_parts.ADS1115 import ADS1115
from custom_parts.BNO055_uart import BNO055
from custom_parts.AS5048A_Process import speed
from custom_parts.OLED import OLED
from custom_parts.CSVDATA import CSVDATA
from custom_parts.pulse_generator import Pulse

import donkeycar as dk

cfg = dk.load_config()
meta = []

V = Vehicle()

# hcsr04 = HCSR04()
# V.add(hcsr04, outputs=['hcsr04'], threaded=True)

ads1115 = ADS1115(coeff_m=cfg.VM_COEFFICIENT, coeff_p=cfg.VP_COEFFICIENT)
V.add(ads1115, outputs=['ads1115/vm', 'ads1115/vp'], threaded=True)

bno055 = BNO055()
V.add(bno055, outputs=["bno055/heading", "bno055/roll", "bno055/pitch", "bno055/sys", "bno055/gyro", "bno055/accel",
                       "bno055/mag", "bno055/ori_x", "bno055/ori_y", "bno055/ori_z", "bno055/ori_w", "bno055/temp_c",
                       "bno055/mag_x", "bno055/mag_y", "bno055/mag_z", "bno055/gyr_x", "bno055/gyr_y", "bno055/gyr_z",
                       "bno055/acc_x", "bno055/acc_y", "bno055/acc_z", "bno055/lacc_x", "bno055/lacc_y",
                       "bno055/lacc_z", "bno055/gra_x", "bno055/gra_y", "bno055/gra_z"], threaded=True)

# as5048a = AS5048A()
# V.add(as5048a, outputs=['as5048a'], threaded=True)
as5048a = speed()
V.add(as5048a, outputs=['as5048a'])


# cam = PiCamera(image_w=cfg.IMAGE_W, image_h=cfg.IMAGE_H, image_d=cfg.IMAGE_DEPTH)
# V.add(cam, inputs=[], outputs=['cam/image_array'], threaded=True)

ctr = get_js_controller(cfg)
V.add(ctr,
      outputs=['user/angle', 'user/throttle', 'user/mode', 'recording'],
      threaded=True)

pulse = Pulse(interval=4, cycle=0.5, length=20, min=0.0, max=0.3)
V.add(pulse, outputs=['user/throttle', 'recording'])

# this throttle filter will allow one tap back for esc reverse
th_filter = ThrottleFilter()
V.add(th_filter, inputs=['user/throttle'], outputs=['user/throttle'])


steering_controller = PCA9685(cfg.STEERING_CHANNEL, cfg.PCA9685_I2C_ADDR, busnum=cfg.PCA9685_I2C_BUSNUM)
steering = PWMSteering(controller=steering_controller,
                       left_pulse=cfg.STEERING_LEFT_PWM,
                       right_pulse=cfg.STEERING_RIGHT_PWM)

throttle_controller = PCA9685(cfg.THROTTLE_CHANNEL, cfg.PCA9685_I2C_ADDR, busnum=cfg.PCA9685_I2C_BUSNUM)
throttle = PWMThrottle(controller=throttle_controller,
                       max_pulse=cfg.THROTTLE_FORWARD_PWM,
                       zero_pulse=cfg.THROTTLE_STOPPED_PWM,
                       min_pulse=cfg.THROTTLE_REVERSE_PWM)

V.add(steering, inputs=['user/angle'])
V.add(throttle, inputs=['user/throttle'])

oled = OLED(OLED_KEY=cfg.OLED_KEY, OLED_PORT=cfg.OLED_PORT)
V.add(oled, inputs=['recording'], threaded=True)

# data save
inputs = ['hcsr04', 'ads1115/vm', 'ads1115/vp', 'as5048a', "bno055/heading", "bno055/roll", "bno055/pitch",
          "bno055/ori_x", "bno055/ori_y", "bno055/ori_z",
          "bno055/ori_w", "bno055/temp_c", "bno055/mag_x", "bno055/mag_y", "bno055/mag_z", "bno055/gyr_x",
          "bno055/gyr_y", "bno055/gyr_z", "bno055/acc_x", "bno055/acc_y", "bno055/acc_z", "bno055/lacc_x",
          "bno055/lacc_y", "bno055/lacc_z", "bno055/gra_x", "bno055/gra_y", "bno055/gra_z",
          'user/angle', 'user/throttle']
types = ['float', 'float', 'float', 'int', 'float', 'float', 'float',
         'float', 'float', 'float',
         'float', 'float', 'float', 'float', 'float', 'float',
         'float', 'float', 'float', 'float', 'float', 'float',
         'float', 'float', 'float', 'float', 'float',
         'float', 'float']

# th = TubHandler(path=cfg.DATA_PATH)
# tub = th.new_tub_writer(inputs=inputs, types=types, user_meta=meta)
# V.add(tub, inputs=inputs, outputs=["tub/num_records"], run_condition='recording')

# one csv file
writer = CSVDATA(path=cfg.DATA_PATH, inputs=inputs)
V.add(writer, inputs=inputs, threaded=True, run_condition='recording')


# run the vehicle for 20 seconds
V.start(rate_hz=cfg.DRIVE_LOOP_HZ,
        max_loop_count=cfg.MAX_LOOPS)
from donkeycar.vehicle import Vehicle
from donkeycar.parts.actuator import PCA9685, PWMSteering, PWMThrottle

from custom_parts.ADS1115 import ADS1115
from custom_parts.BNO055 import BNO055
from custom_parts.AS5048A_Process import speed
from custom_parts.OLED import OLED
from custom_parts.CSVDATA import CSVDATA
from custom_parts.pulse_generator import Pulse

import donkeycar as dk

cfg = dk.load_config()
meta = []
V = Vehicle()

pulse = Pulse()
V.add(pulse, outputs=['user/throttle', 'recording'])


throttle_controller = PCA9685(cfg.THROTTLE_CHANNEL, cfg.PCA9685_I2C_ADDR, busnum=cfg.PCA9685_I2C_BUSNUM)
throttle = PWMThrottle(controller=throttle_controller,
                       max_pulse=cfg.THROTTLE_FORWARD_PWM,
                       zero_pulse=cfg.THROTTLE_STOPPED_PWM,
                       min_pulse=cfg.THROTTLE_REVERSE_PWM)
V.add(throttle, inputs=['user/throttle'])


ads1115 = ADS1115(coeff_m=cfg.VM_COEFFICIENT, coeff_p=cfg.VP_COEFFICIENT)
V.add(ads1115, outputs=['ads1115/vm', 'ads1115/vp'], threaded=True)

as5048a = speed()
V.add(as5048a, outputs=['as5048a'])

oled = OLED(OLED_KEY=cfg.OLED_KEY, OLED_PORT=cfg.OLED_PORT)
V.add(oled, inputs=['recording'])


# data save
inputs = ['ads1115/vm', 'ads1115/vp', 'as5048a',
          'user/throttle']
types = ['float', 'float', 'float',
         'float']

# one csv file
writer = CSVDATA(path=cfg.DATA_PATH, inputs=inputs)
V.add(writer, inputs=inputs, threaded=True, run_condition='recording')

# run the vehicle for 20 seconds
V.start(rate_hz=cfg.DRIVE_LOOP_HZ,
        max_loop_count=cfg.MAX_LOOPS)




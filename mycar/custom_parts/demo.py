import time
import board
import busio
import donkeycar as dk
from donkeycar.vehicle import Vehicle
from display import display
from pi_camera import PiCamera, CameraDisplay, WarpCameraDisplay
from perspective_warp import perspective_warp
#from donkeycar.parts.camera import PiCamera
import time
from docopt import docopt
import numpy as np
'''
V = Vehicle()
C = PiCamera()
V.add(C, outputs=["cameraimage"], threaded = False)
D = CameraDisplay()
V.add(D, inputs=["cameraimage"])
V.start()
'''

V = Vehicle()
C = PiCamera()
V.add(C, outputs=["cameraimage"], threaded = False)
P = perspective_warp()
V.add(P, inputs=["cameraimage"], outputs=["warped"], threaded = False)
W = WarpCameraDisplay()
V.add(W, inputs=["warped"], threaded = False)
V.start()


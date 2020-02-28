from donkeycar.parts.controller import Joystick

joystick = Joystick() # uses the connected joystick at /dev/input/js0

joystick.init() # Initialize

joystick.show_map() # Will give you a list of axes and buttons detected.

# Now you can use the controller and check for the outputs. This will
# tell you which buttons and axes are active when you are using the
# controller.
while True:
    joystick.poll()

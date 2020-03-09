### How to disable internal bluetooth on raspberry pi  
```console
sudo vim /boot/config.txt
```
Add following to last line:  
```
# Disable Bluetooth
dtoverlay = pi3-miniuart-bt
```
Then type command:  
```console
sudo systemctl stop hciuart
sudo systemctl disable hciuart
```
Now check your usb adapter is found:  
```console
(env) pi@raspberrypi:~ $ lsusb
Bus 001 Device 003: ID 0a12:0001 Cambridge Silicon Radio, Ltd Bluetooth Dongle (HCI mode)
....etc
```
Check hci device is on:  
```console
(env) pi@raspberrypi:~ $ sudo hciconfig -a
hci0:	Type: Primary  Bus: USB
	BD Address: 00:1A:7D:DA:71:13  ACL MTU: 310:10  SCO MTU: 64:8
	UP RUNNING 
	RX bytes:2137 acl:0 sco:0 events:116 errors:0
	TX bytes:4973 acl:0 sco:0 commands:116 errors:0
	Features: 0xff 0xff 0x8f 0xfe 0xdb 0xff 0x5b 0x87
	Packet type: DM1 DM3 DM5 DH1 DH3 DH5 HV1 HV2 HV3 
	Link policy: RSWITCH HOLD SNIFF PARK 
	Link mode: SLAVE ACCEPT 
	Name: 'raspberrypi #1'
	Class: 0x000000
	Service Classes: Unspecified
	Device Class: Miscellaneous, 
	HCI Version: 4.0 (0x6)  Revision: 0x22bb
	LMP Version: 4.0 (0x6)  Subversion: 0x22bb
	Manufacturer: Cambridge Silicon Radio (10)
```
### How to pair PS3 controller to raspberry pi  
Download required libs and setup:  
```console
sudo apt-get install bluetooth libbluetooth3 libusb-dev
sudo systemctl enable bluetooth.service
sudo usermod -G bluetooth -a pi
```
Plug in PS3 controller with cable, and run:  
```console
wget http://www.pabr.org/sixlinux/sixpair.c
gcc -o sixpair sixpair.c -lusb
sudo ./sixpair
Current Bluetooth master: 00:1a:7d:da:71:13
Setting master bd_addr to 00:1a:7d:da:71:13
```
Check cable connection:  
```console
(env) pi@raspberrypi:~ $ lsusb
Bus 001 Device 004: ID 054c:0268 Sony Corp. Batoh Device / PlayStation 3 Controller
...etc
```
Now enter bluetoothctl:  
```console
(env) pi@raspberrypi:~ $ bluetoothctl
Agent registered
[CHG] Controller 00:1A:7D:DA:71:13 Discoverable: no
[bluetooth]# agent on
Agent is already registered
[bluetooth]# pairable on
Changing pairable on succeeded
[bluetooth]# devices
Device 04:38:75:80:63:25 Sony PLAYSTATION(R)3 Controller
[bluetooth]# trust 04:38:75:80:63:25
Changing 04:38:75:80:63:25 trust succeeded
[bluetooth]# default-agent
Default agent request successful
[bluetooth]# quit
```
Then unplug cable and try to connect the controller:  
```console
(env) pi@raspberrypi:~ $ ls /dev/input/js0
/dev/input/js0
```
Now start driving:  
```console
(env) pi@raspberrypi:~/mycar $ python manage.py drive --js
using donkey v3.1.1 ...
loading config file: /home/pi/mycar/config.py
loading personal config over-rides

config loaded
cfg.CAMERA_TYPE PICAM
cfg.CAMERA_TYPE PICAM
PiCamera loaded.. .warming camera
Adding part PiCamera.
Adding part PS3JoystickController.
Adding part ThrottleFilter.
Adding part PilotCondition.
Adding part RecordTracker.
Adding part ImgPreProcess.
Adding part DriveMode.
Adding part AiLaunch.
Adding part AiRunCondition.
Init ESC
Adding part PWMSteering.
Adding part PWMThrottle.
Tub does NOT exist. Creating new tub...
New tub created at: /home/pi/mycar/data/tub_21_20-02-27
Adding part TubWriter.
You can now move your joystick to drive your car.
Joystick Controls:
+------------------+---------------------------+
|     control      |           action          |
+------------------+---------------------------+
|      select      |        toggle_mode        |
|      circle      | show_record_acount_status |
|     triangle     |    erase_last_N_records   |
|      cross       |       emergency_stop      |
|     dpad_up      |   increase_max_throttle   |
|    dpad_down     |   decrease_max_throttle   |
|      start       |  toggle_constant_throttle |
|        R1        |   chaos_monkey_on_right   |
|        L1        |    chaos_monkey_on_left   |
|        R2        |      enable_ai_launch     |
| left_stick_horz  |        set_steering       |
| right_stick_vert |        set_throttle       |
+------------------+---------------------------+
Starting vehicle...
Opening /dev/input/js0...
Device name: Sony PLAYSTATION(R)3 Controller
```
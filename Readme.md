## Installation
### Donkey car setup
1. `sudo raspi-config`\
   enable `Interfacing Options` - `I2C`\
   enable `Interfacing Options` - `SPI`\
   enable `Interfacing Options` - `Camera`\
   select `Advanced Options` - `Expand Filesystem`\
   `<Finish>`
2. Reference : http://docs.donkeycar.com/guide/robot_sbc/setup_raspberry_pi/ \
   Step 8-11

### Modify `/boot/config.txt`
1. Enable I2C6

    add 2 rows into /boot/config.txt  \
    `sudo vim /boot/config.txt`
    ```
    # Additional overlays and parameters are documented /boot/overlays/README
    dtoverlay=i2c6
    ```

2. Set Input GPIO

    add 2 rows into /boot/config.txt \
    `sudo vim /boot/config.txt`
    ```
    # GPIO
    gpio=13,16,19,20,21,26=ip
    ```
   
### Install other dependencies
1. using apt command
    ```
    sudo apt install libgpiod2
    ```

2. using pip command
    ```
    pip install -r requirements.txt
    ```

## Test
Run test code in `TEST_CODE` folder

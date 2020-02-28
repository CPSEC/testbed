# Simple demo of reading and writing the time for the DS3231 real-time clock.
# Change the if False to if True below to set the time, otherwise it will just
# print the current date and time every second.  Notice also comments to adjust
# for working with hardware vs. software I2C.

import time
import board
# For hardware I2C (M0 boards) use this line:
import busio as io
# Or for software I2C (ESP8266) use this line instead:
#import bitbangio as io

import adafruit_ds3231

from datetime import datetime


i2c = io.I2C(board.SCL, board.SDA)  # Change to the appropriate I2C clock & data
                                    # pins here!

# Create the RTC instance:
rtc = adafruit_ds3231.DS3231(i2c)

# Lookup table for names of days (nicer printing).
days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")


#pylint: disable-msg=bad-whitespace
#pylint: disable-msg=using-constant-test
if True:   # change to True if you want to set the time!
    year = (int)(datetime.now().year)
    mon = (int)(datetime.now().month)
    day = (int)(datetime.now().day)
    hour = (int)(datetime.now().hour)
    minu = (int)(datetime.now().minute)
    sec = (int)(datetime.now().second)
    #                     year, mon, date, hour,  min, sec, wday, yday, isdst
    t = time.struct_time((year, mon,  day, hour, minu, sec,    0,   -1,    -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time
    print("Setting time to:", t)     # uncomment for debugging
    rtc.datetime = t
    print()
#pylint: enable-msg=using-constant-test
#pylint: enable-msg=bad-whitespace

# Main loop:
while True:
    t = rtc.datetime
    #print(t)     # uncomment for debugging
    print("The date is {} {}/{}/{}".format(days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year))
    print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))
    time.sleep(1) # wait a second


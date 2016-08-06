### Author: EMF Badge team
### Description: Shows all the sponsors that have helped make this badge possible
### Category: Other
### License: MIT

import ugfx, pyb, buttons
from imu import IMU
import onboard
import wifi
import random

def batteryled():
    ledg = pyb.LED(2)
    bat_percent = max(0,onboard.get_battery_percentage())
    bat_percent = (2*bat_percent) + 50
    ledg.intensity(bat_percent)

def wifiled():
    ledr = pyb.LED(1)
    rssi = wifi.nic().get_rssi()
    intensuty = (rssi+100)*3
    ledr.intensity(intensuty)


ugfx.init()
ugfx.clear()
buttons.init()
ugfx.set_default_font(ugfx.FONT_NAME)

imu=IMU()
neo = pyb.Neopix(pyb.Pin("PB13"))
neo.display(0x04040404)
ledg = pyb.LED(2)
ival = imu.get_acceleration()
if ival['y'] < 0:
	ugfx.orientation(0)
else:
	ugfx.orientation(180)

def screen_1():
    ugfx.display_image(0, 0, "apps/sponsors/splash3.gif")

def screen_2():
    color = random.randint(0, 0xffffff)
    ugfx.clear(ugfx.html_color(color))
    ugfx.display_image(0, 0, "apps/sponsors/sponsors2.gif")

def screen_3():
    ugfx.clear(ugfx.html_color(0x7c1143))
    ugfx.text(27, 90, "@tofu_li", ugfx.WHITE)

SCREENS = [screen_1, screen_3]
SCREEN_DURATION = 2000


screen_index = -1
next_change = 0
next_color_change = 0
while True:
    if pyb.millis() > next_change:
        screen_index = (screen_index + 1) % len(SCREENS)
        SCREENS[screen_index]()
        next_change = pyb.millis() + SCREEN_DURATION
        next_color_change = pyb.millis()  + (SCREEN_DURATION/10)
    elif pyb.millis() > next_color_change:
        SCREENS[screen_index]()
        next_color_change = pyb.millis()  + (SCREEN_DURATION/10)

    pyb.wfi()
    if buttons.is_triggered("BTN_MENU"):
        break;
    elif buttons.is_triggered("BTN_A"):
        wifiled()
    elif buttons.is_triggered("BTN_B"):
        batteryled()
    elif buttons.is_triggered("JOY_CENTER"):
        pass


    ival = imu.get_acceleration()
    if ival['y'] < 0:
        ugfx.orientation(0)
    else:
        ugfx.orientation(180)

ugfx.clear()




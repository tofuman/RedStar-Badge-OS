### Author: EMF Badge team
### Description: Shows all the sponsors that have helped make this badge possible
### Category: Other
### License: MIT

import ugfx, pyb, buttons
from imu import IMU
import onboard
import wifi
import dialogs
from music import hymne

def batteryled(enable):
    ledg = pyb.LED(2)
    if enable:
        bat_percent = min( 100, max(0,onboard.get_battery_percentage()))
        bat_percent = int(bat_percent * 2.5)
        ledg.intensity(bat_percent)
        print("barrery : "  + str(bat_percent))
    else:
        ledg.intensity(255)
    return not batteryled_status

def wifiled(enable):
    ledr = pyb.LED(1)
    if enable:
        rssi = wifi.nic().get_rssi()
        intensuty = (rssi+100)*3
        ledr.intensity(intensuty)
        print("Rssi: " + str(rssi))
    else:
        ledr.intensity(255)


ugfx.init()
ugfx.clear()
buttons.init()
ugfx.set_default_font(ugfx.FONT_NAME)
ugfx.backlight(100)

imu=IMU()
neo = pyb.Neopix(pyb.Pin("PB13"))
neo.display(0x04040404)
ledg = pyb.LED(2)
ival = imu.get_acceleration()
if ival['y'] < 0:
	ugfx.orientation(0)
else:
	ugfx.orientation(180)

def kim(foo):
    ugfx.display_image(0, 0, "apps/home/kim.gif")

def nick_screen(container_handle):
    if not container_handle:
        container_handle = ugfx.Container(0, 0, 320, 240)
    container_handle.area(0, 0, 320, 240, ugfx.html_color(pyb.rng()%0xffffff))
    ugfx.display_image(0, 0, "apps/sponsors/splash3.gif")

    container_handle.show()
    return container_handle

def twitter(container_handle):
    if not container_handle:
        container_handle = ugfx.Container(0, 0, 320, 240)
        container_handle.area(0, 0, 320, 240, ugfx.html_color(0))
    container_handle.text(27, 90, "@tofu_li", ugfx.GREEN)
    container_handle.show()

SCREENS = [nick_screen, kim]
SCREEN_DURATION = 20000

ugfx.init()
imu=IMU()
neo = pyb.Neopix(pyb.Pin("PB13"))
neo.display(0x04040404)
ledg = pyb.LED(2)
ival = imu.get_acceleration()
if ival['y'] < 0:
	ugfx.orientation(0)
else:
	ugfx.orientation(180)


buttons.init()
if not onboard.is_splash_hidden():
	splashes = ["apps/home/kim.gif"]
	for s in splashes:
		ugfx.display_image(0,0,s)
		hymne()
		delay = 2000
		while delay:
			delay -= 1
			if buttons.is_triggered("BTN_MENU"):
				break;
			if buttons.is_triggered("BTN_A"):
				break;
			if buttons.is_triggered("BTN_B"):
				break;
			if buttons.is_triggered("JOY_CENTER"):
				break;
			pyb.delay(1)


onboard.hide_splash_on_next_boot(False)

ugfx.set_default_style(dialogs.default_style_badge)

sty_tb = ugfx.Style(dialogs.default_style_badge)
sty_tb.set_enabled([ugfx.WHITE, ugfx.html_color(0xA66FB0), ugfx.html_color(0x5e5e5e), ugfx.RED])
sty_tb.set_background(ugfx.html_color(0xA66FB0))

orientation = ugfx.orientation()

screen_index = -1
next_change = 0
next_color_change = 0
container = None
batteryled_status = False

while True:
    if pyb.millis() > next_change:
        screen_index = (screen_index + 1) % len(SCREENS)
        container = SCREENS[screen_index](None)
        next_change = pyb.millis() + SCREEN_DURATION
        next_color_change = pyb.millis()  + (SCREEN_DURATION/10)
    elif pyb.millis() > next_color_change and SCREENS[screen_index] == nick_screen:
        container = SCREENS[screen_index](container)
        next_color_change = pyb.millis()  + (SCREEN_DURATION/10)
        batteryled_status = batteryled(batteryled_status)

    pyb.wfi()
    if buttons.is_triggered("BTN_MENU"):
        break;

    # if buttons.is_triggered("BTN_A"):
    #     wifiled(True)
    # else:
    #     wifiled(False)

    if buttons.is_triggered("BTN_A"):
        hymne()

    if buttons.is_triggered("JOY_CENTER"):
        pass


    ival = imu.get_acceleration()
    if ival['y'] < 0:
        ugfx.orientation(0)
    else:
        ugfx.orientation(180)

ugfx.clear()




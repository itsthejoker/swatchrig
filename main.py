"""
Notes:
    the switch is / will be connected to GPIO2 / pin 3
    the mosfet is / will be connected to GPIO3 / pin 5
    switch ground pin: 9
    mosfet ground pin: either 9 or 14
"""
import os
import subprocess
from datetime import datetime
from signal import pause

from gpiozero import Button

# this is not a native field for the Button class, but is used to allow mapping
# a single event and a held event to the same entity.
Button.was_held = False

button = Button(2, hold_time=5)
todays_folder = str(datetime.now().date())

os.chdir("/share")
if not os.path.exists(todays_folder):
    os.mkdir(todays_folder)

os.chdir(todays_folder)


def shutdown():
    subprocess.check_call(['sudo', 'poweroff'])


def take_picture():
    subprocess.call(
        ["raspistill", "-o", f"{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.jpg"]
    )

def held(btn):
    btn.was_held = True

def released(btn):
    if btn.was_held:
        shutdown()
        return
    take_picture()


button.when_held = held
button.when_released = released

pause()

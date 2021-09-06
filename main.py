"""
Notes:
    the switch is connected to GPIO2 / pin 3
    the mosfet is connected to GPIO3 / pin 5
    switch ground pin: 9
    mosfet ground pin: 14
"""
import os
import subprocess
from datetime import datetime
from signal import pause

from gpiozero import Button, PWMOutputDevice

# By design, you can't modify attributes of the gpiozero classes after
# initialization, so we have to define our custom attribute beforehand.
Button.was_held = False

button = Button(2, hold_time=5)
mosfet = PWMOutputDevice(3)

todays_folder = str(datetime.now().date())
root_folder = "/home/pi/Pictures"
PICTURE_ROOT = os.path.join(root_folder, todays_folder)

if not os.path.exists(PICTURE_ROOT):
    os.mkdir(PICTURE_ROOT)


def shutdown():
    subprocess.check_call(['sudo', 'poweroff'])


def take_picture():
    filename = os.path.join(
        PICTURE_ROOT, f"{datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}.jpg"
    )
    mosfet.on()
    subprocess.call(
        ["raspistill", "-r", "-o", filename]
    )
    mosfet.off()
    # TODO: add pidng conversion with custom profile


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

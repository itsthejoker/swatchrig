"""
Notes:
    the switch is connected to GPIO2 / pin 3
    the mosfet is connected to GPIO3 / pin 5
    switch ground pin: 9
    mosfet ground pin: 14
"""
import os
import subprocess
import shlex
import time
from datetime import datetime
from signal import pause

from pidng.core import Profile, RPICAM2DNG
from gpiozero import Button, PWMOutputDevice


custom_profile = Profile(
    name="default",
    profile_name="Raspberry Pi HQ Camera Custom Profile",
    as_shot_neutral=None,
    # fmt: off
    ccm1=[  # from custom profile
        [3501, 10000], [576, 10000], [-547, 10000],
        [-10669, 10000], [18920, 10000], [1658, 10000],
        [-3479, 10000], [4305, 10000], [6034, 10000],
    ],
    ccm2=[
        [4262, 10000], [-388, 10000], [-326, 10000],
        [-5086, 10000], [13148, 10000], [2129, 10000],
        [-1186, 10000], [2345, 10000], [5652, 10000]
    ],
    # fmt: on
    illu1=17,
    illu2=21,
)
command = (
    "xterm -fullscreen"
    " -fa 'Monospace'"
    " -fs 14"
    " -en en_US.UTF-8"
    " -e '/home/pi/app/.venv/bin/python /home/pi/app/extras/{}.py'"
)
processing_cmd = command.format('processing')
converting_cmd = command.format('converting')
processing_cmd = shlex.split(processing_cmd)
converting_cmd = shlex.split(converting_cmd)

RpiCam = RPICAM2DNG(profile=custom_profile)

# By design, you can't modify attributes of the gpiozero classes after
# initialization, so we have to define our custom attribute beforehand.
Button.was_held = False
Button.release_time = None

button = Button(2, hold_time=1)
mosfet = PWMOutputDevice(3)

todays_folder = str(datetime.now().date())
root_folder = "/home/pi/Pictures"
PICTURE_ROOT = os.path.join(root_folder, todays_folder)

if not os.path.exists(PICTURE_ROOT):
    os.mkdir(PICTURE_ROOT)


def shutdown():
    subprocess.check_call(['sudo', 'poweroff'])


def convert(filename):
    p = subprocess.Popen(converting_cmd, stdout=subprocess.PIPE, shell=False, env={"DISPLAY": ":0.0"})
    RpiCam.convert(filename)
    p.terminate()


def take_picture():
    filename = os.path.join(
        PICTURE_ROOT, f"{datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}.jpg"
    )
    mosfet.on()
    subprocess.call(
        ["raspistill", "-r", "-o", filename]
    )
    mosfet.off()
    convert(filename)
    os.remove(filename)


def process_photos():
    p = subprocess.Popen(processing_cmd, stdout=subprocess.PIPE, shell=False, env={"DISPLAY": ":0.0"})

    subprocess.call(
        f"mogrify -format jpg {os.path.join(PICTURE_ROOT, '*.dng')}".split()
    )
    p.terminate()


def held(btn):
    btn.was_held = True


# noinspection PyUnusedLocal
def pressed(*btn):
    # can't use btn.held_time because the library only makes it available while
    # the button is physically being pressed, which isn't what we want.
    global press_time
    press_time = time.time()


def released(btn):
    global press_time

    if btn.was_held:
        time_held = int(time.time() - press_time)

        if time_held >= 5:
            shutdown()
        # if it's not enough to trigger a shutdown but it was enough to count
        # as held, then we'll start processing.
        process_photos()
        btn.was_held = False
        return
    take_picture()


if __name__ == "__main__":
    button.when_pressed = pressed
    button.when_held = held
    button.when_released = released

    pause()

"""
Notes:
    the switch is connected to GPIO2 / pin 3
    the mosfet is connected to GPIO3 / pin 5
    switch ground pin: 9
    mosfet ground pin: 14

    screen mods: in /etc/lightdm/lightdm.conf under [Seat:*]
    # don't sleep the screen and also remove the cursor
    xserver-command=X -s 0 -dpms -nocursor

"""
import os
import subprocess
import shlex
import time
from datetime import datetime
from signal import pause

from gpiozero import Button, PWMOutputDevice


command = (
    "xterm -fullscreen"
    " -fa 'Monospace'"
    " -fs 14"
    " -en en_US.UTF-8"
    " -e '/home/pi/app/.venv/bin/python /home/pi/app/extras/{}.py'"
)

processing_cmd = shlex.split(command.format('processing'))
converting_cmd = shlex.split(command.format('converting'))
main_screen_cmd = shlex.split(command.format('mainscreen'))
error_cmd = shlex.split(command.format('error'))

POPEN_SETTINGS = {
    'stdout': subprocess.PIPE,
    'shell': False,
    'env': {"DISPLAY": ":0.0"}
}

# By design, you can't modify attributes of the gpiozero classes after
# initialization, so we have to define our custom attribute beforehand.
Button.was_held = False
Button.release_time = None

button = Button(2, hold_time=1.5)
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
    # why these numbers? IDK. Found 'em over here and they produce a usable
    # starting point:
    # https://github.com/thomasjacquin/allsky/issues/791#issuecomment-968330633
    command = f"libcamera-still -r -f -o {filename} --awbgains 3.65,1.5"
    subprocess.call(shlex.split(command))
    mosfet.off()


def sync_photos():
    # note: this requires setting up ssh key access
    p = subprocess.Popen(processing_cmd, **POPEN_SETTINGS)
    response = os.system("ping -c 1 -w2 " + "storagebox.local" + " > /dev/null 2>&1")
    if response == 0:
        command = (
            "rsync -avr --info=progress2 /home/pi/Pictures/"
            " root@storagebox.local:/mnt/user/images/swatches/"
        )
        subprocess.call(shlex.split(command))
        p.terminate()
    else:
        # swap out screens for the error one
        p.terminate()
        error = subprocess.Popen(error_cmd, **POPEN_SETTINGS)
        time.sleep(5)
        error.terminate()


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
        # as held, then we'll try to sync.
        sync_photos()
        btn.was_held = False
        return
    take_picture()


if __name__ == "__main__":
    subprocess.Popen(main_screen_cmd, **POPEN_SETTINGS)

    button.when_pressed = pressed
    button.when_held = held
    button.when_released = released

    pause()

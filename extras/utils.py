# -*- coding: utf-8 -*-
import random
import os
import signal

dudes = [
    "ᕙ(⇀‸↼‵‵)ᕗ",
    "(ง •̀_•́)ง",
    "ᕦ(ò_óˇ)ᕤ",
    "୧(๑•̀ㅁ•́๑)૭✧",
    "ᕦ(･ㅂ･)ᕤ",
    "ᕕ( ᐛ )ᕗ",
    "(ง •̀_•́)ง",
    "(ง˙o˙)ว",
    "(๑•̀ㅂ•́)و✧",
    "(;´Д`)",
    "(ノ￣ー￣)ノ",
    "(✿◡‿◡)",
    "(－.－)...zzz",
    "｡^‿^｡",
    "＼（＾∀＾）メ（＾∀＾）ノ",
    "ಠ_ಠ",
    "（*＾ワ＾*）",
    "(￣～￣；)",
    "(╯‵□′)╯Boom！•••*～●"
]

def get_dude():
    return random.choice(dudes)


def print_message(message, initial_newlines=4, show_dude=True):
    width, height = os.get_terminal_size()

    for _ in range(initial_newlines):
        print()
    for line in message.split('\n'):
        print(line.rjust(int((width - len(line)) / 2 + len(line))))

    if show_dude:
        dude = get_dude()
        print(dude.rjust(int((width - len(dude)) / 2 + len(dude))))

    # this should be killed mercilessly by the subprocess, so just pause until the end of time.
    signal.pause()

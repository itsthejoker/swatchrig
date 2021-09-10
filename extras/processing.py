import os
import random
import signal

width, height = os.get_terminal_size()

processing = """
                                   _                   
 _ __  _ __ ___   ___ ___  ___ ___(_)_ __   __ _       
| '_ \| '__/ _ \ / __/ _ \/ __/ __| | '_ \ / _` |      
| |_) | | | (_) | (_|  __/\__ \__ \ | | | | (_| |_ _ _ 
| .__/|_|  \___/ \___\___||___/___/_|_| |_|\__, (_|_|_)
|_|                                        |___/       
"""
for line in processing.split('\n'):
    print(line.rjust(int((width - 56) / 2 + 56)))

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

dude = random.choice(dudes)
print(dude.rjust(int((width - len(dude)) / 2 + len(dude))))

# this should be killed mercilessly by the subprocess, so just pause until the end of time.
signal.pause()

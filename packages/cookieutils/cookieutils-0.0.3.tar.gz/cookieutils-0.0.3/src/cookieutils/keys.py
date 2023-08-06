import os, sys
from cookieutils.key import CKey
import time
import cookieutils

if os.name=='nt': # windows
  from pynput import keyboard
else: #unix
  import tty,termios

operating_system = cookieutils.get_os()



def __presets(key):
    map = {
        "backspace": CKey.backspace,
        "enter":  CKey.enter,
        "space":  CKey.space,
        "tab":   CKey.tab,
        "esc":  CKey.esc,
        "up":  CKey.up,
        "down":  CKey.down,
        "right":  CKey.right,
        "left":  CKey.left
    }
    if key.name in map.keys():
        return map[key.name]
    else:
        return False


def __getkey():
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            b = os.read(sys.stdin.fileno(), 3).decode()
            if len(b) == 3:
                k = ord(b[2])
            else:
                k = ord(b)
            key_mapping = {
                127: CKey.backspace,
                10:  CKey.enter,
                32:  CKey.space,
                9:   CKey.tab,
                27:  CKey.esc,
                65:  CKey.up,
                66:  CKey.down,
                67:  CKey.right,
                68:  CKey.left
            }
            return key_mapping.get(k, chr(k))
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def get():
    if operating_system == "windows":
        time.sleep(0.3) # gives it some time so it does not pick up missinputs, also prevents it from imidently shutting off for some reason lol idk why
        with keyboard.Events() as events: # if on a windows system
            event = events.get()
            if event is None:
                raise ValueError('Uh oh. somthing just went wrong with the event. contact the dev lol, CODE: 001')
            else:
                if event.__class__ == keyboard.Events.Press:
                    try:
                        return {"type":"letter", "data":event.key.char}
                    except AttributeError: # if it is a letter or not
                        return {"type":"key", "data":__presets(event.key)}


    elif operating_system == "unix": # if on a unix system
        try:
            k = __getkey()
            try:
                if k.name:
                    return {"type":"key", "data":k}
            except AttributeError: # check if it is a letter or not
                    return {"type":"letter", "data":str(k)}
        except (KeyboardInterrupt):
            os.system('stty sane')
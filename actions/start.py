import os
import cv2
import numpy as np
from pynput import keyboard
from mss import mss
from threading import Thread
from colorama import Fore, Style
from utils.window_box import get_rect_by_name
from core.storage import Storage


def start():
    os.system('cls')
    print('{}Lightning AI started. Press {}Pause Break{} to stop.{}'.format(
        Fore.GREEN,
        Fore.YELLOW + Style.BRIGHT,
        Style.RESET_ALL + Fore.GREEN,
        Style.RESET_ALL
    ))

    def on_press(key):
        if key == keyboard.Key.pause:
            Storage().set_data('lightning_started', False)

    sct = mss()
    listener = keyboard.Listener(on_press=on_press)
    thread = Thread(target=listener.start)
    thread.start()

    Storage().set_data('lightning_started', True)
    while Storage().data['lightning_started']:
        box = get_rect_by_name('Code.exe')
        sct_img = sct.grab(box)

        img = np.array(sct_img)
        res = cv2.resize(img, (960, 540), interpolation=cv2.INTER_CUBIC)

        cv2.imshow('screen', res)
        cv2.waitKey(1)

    cv2.destroyAllWindows()
    thread.join()

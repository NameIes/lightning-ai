import os
import cv2
import numpy as np
from pynput import keyboard
from mss import mss
from threading import Thread
from colorama import Fore, Style
from ultralytics import YOLO
from utils.window_box import get_rect_by_name
from core.storage import Storage


def place_results(results, resized):
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0]
            cls = box.cls[0]

            cv2.rectangle(resized, (x1, y1), (x2, y2), (0, 255, 0), 2)

            label = f'{cls}: {conf:.2f}'
            cv2.putText(resized, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


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
        box = get_rect_by_name('firefox.exe')
        sct_img = sct.grab(box)
        img = np.array(sct_img)
        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        resized = cv2.resize(img, (960, 544), interpolation=cv2.INTER_CUBIC)

        model = YOLO('./models/pretraining.pt')
        results = model(resized, imgsz=(960, 544))[0]

        place_results(results, resized)

        cv2.imshow('screen', resized)
        cv2.waitKey(1)

    cv2.destroyAllWindows()
    thread.join()

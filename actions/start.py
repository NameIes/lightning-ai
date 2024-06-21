import os
import cv2
import numpy as np
from typing import Optional
from pynput import keyboard
from mss import mss
from threading import Thread
from colorama import Fore, Style
from ultralytics import YOLO
from core.storage import Storage
from utils.capture import take_screenshot, resize_image


def print_info() -> None:
    os.system('cls')
    print('{}Lightning AI started. Press {}Pause Break{} to stop.{}'.format(
        Fore.GREEN,
        Fore.YELLOW + Style.BRIGHT,
        Style.RESET_ALL + Fore.GREEN,
        Style.RESET_ALL
    ))


def on_press(key) -> None:
    if key == keyboard.Key.pause:
        Storage().set_data('lightning_started', False)


def start_keyboard_listener() -> Thread:
    listener = keyboard.Listener(on_press=on_press)
    thread = Thread(target=listener.start)
    thread.start()

    return thread


def transform_YOLO_boxes(boxes: Optional[np.array], orig_size: tuple, new_size: tuple) -> list[int, int, int, int, float, int]:
    orig_width, orig_height = orig_size
    new_width, new_height = new_size
    scale_x = orig_width / new_width
    scale_y = orig_height / new_height

    transformed_boxes = []
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        conflidense, class_id = box.conf[0], box.cls[0]
        x1 = int(x1 * scale_x)
        x2 = int(x2 * scale_x)
        y1 = int(y1 * scale_y)
        y2 = int(y2 * scale_y)
        transformed_boxes.append([x1, y1, x2, y2, conflidense, class_id])

    return transformed_boxes


def place_results(boxes: list, img: cv2.typing.MatLike) -> None:
    for box in boxes:
        x1, y1, x2, y2, conflidense, class_id = box
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f'{class_id}: {conflidense:.2f}'
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


def start() -> None:
    sct = mss()
    print_info()
    thread = start_keyboard_listener()

    Storage().set_data('lightning_started', True)
    while Storage().data['lightning_started']:
        img = take_screenshot(sct, 'firefox.exe')
        resized_image, orig_size, new_size = resize_image(img)

        model = YOLO('./models/pretraining.pt')
        results = model(resized_image, imgsz=new_size)[0]

        boxes = results.boxes.cpu().numpy()
        transformed_boxes = transform_YOLO_boxes(boxes, orig_size, new_size)

        place_results(transformed_boxes, img)

        cv2.imshow('screen', img)
        cv2.waitKey(1)

    cv2.destroyAllWindows()
    thread.join()

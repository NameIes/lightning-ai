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
from utils.move_mouse import move_mouse, mouse_click
from core.rect import Rect


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
    if key == keyboard.Key.f8:
        st = Storage()
        if st.data['team'] == 'off':
            st.set_data('team', 'ct')
        elif st.data['team'] == 'ct':
            st.set_data('team', 't')
        elif st.data['team'] == 't':
            st.set_data('team', 'all')
        elif st.data['team'] == 'all':
            st.set_data('team', 'off')

        print(Fore.GREEN + 'Team: ' + st.data['team'] + Style.RESET_ALL)


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


def vector_length(x1: int, y1: int, x2: int, y2: int) -> float:
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def is_cursor_in_rect(cur, rect):
    return cur[0] >= rect.x1 and cur[0] <= rect.x2 and cur[1] >= rect.y1 and cur[1] <= rect.y2


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
    model = YOLO('./models/best.pt')
    model.to('cuda')
    while Storage().data['lightning_started']:
        if Storage().data['team'] == 'off':
            continue
        img = take_screenshot(sct, 'cs2.exe')
        resized_image, orig_size, new_size = resize_image(img)

        results = model(resized_image, imgsz=new_size, verbose=False)[0]

        boxes = results.boxes.cpu().numpy()
        transformed_boxes = transform_YOLO_boxes(boxes, orig_size, new_size)

        # ct - 1
        # ct_head - 2
        # t - 3
        # t_head - 4
        rects = []
        for box in transformed_boxes:
            if (int(box[5]) in (1, 2) and Storage().data['team'] == 't') or Storage().data['team'] == 'all':
                rects.append(Rect(box[0], box[1], box[2], box[3], box[4], box[5]))
            if int(box[5]) in (3, 4) and Storage().data['team'] == 'ct' or Storage().data['team'] == 'all':
                rects.append(Rect(box[0], box[1], box[2], box[3], box[4], box[5]))

        half = (orig_size[0] // 2, orig_size[1] // 2)
        rects.sort(key=lambda x: vector_length(x.get_center()[0], x.get_center()[1], half[0], half[1]))

        if rects:
            center = rects[0].get_center()
            x, y = center[0] - half[0], center[1] - half[1]
            if is_cursor_in_rect(half, rects[0]):
                move_mouse(x // 3, y)
            else:
                move_mouse(x, y)
            mouse_click()

        # place_results(transformed_boxes, img)
        # cv2.imshow('screen', img)
        # cv2.waitKey(1)

    cv2.destroyAllWindows()
    thread.join()

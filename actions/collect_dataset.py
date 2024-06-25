import os
import cv2
from mss import mss
from colorama import Fore, Style
from pathlib import Path
from pynput import keyboard
from threading import Thread
from time import sleep
from core.storage import Storage
from core.detect import YOLODetection


def print_info() -> None:
    os.system('cls')
    print('{}Collecting dataset. Press {}Pause Break{} to stop.{}'.format(
        Fore.GREEN,
        Fore.YELLOW + Style.BRIGHT,
        Style.RESET_ALL + Fore.GREEN,
        Style.RESET_ALL
    ))


def on_press(key) -> None:
    if key == keyboard.Key.pause:
        Storage()['lightning_started'] = False


def start_keyboard_listener() -> Thread:
    listener = keyboard.Listener(on_press=on_press)
    thread = Thread(target=listener.start)
    thread.start()

    return thread


def get_or_create_folder() -> Path:
    datasets = Storage().data['base_dir'] / 'datasets' / 'collected'

    if not datasets.exists():
        datasets.mkdir(parents=True)

    with open(datasets / '.gitkeep', 'w') as f:
        f.write('')

    subfolders_names = [int(name.name) for name in datasets.iterdir() if name.is_dir() and name.name.isdigit()]
    subfolders_names.append(0)

    new_subfolder_name = max(subfolders_names) + 1
    new_subfolder = datasets / str(new_subfolder_name)
    new_subfolder.mkdir()

    return new_subfolder


def collect_dataset() -> None:
    print_info()

    dataset_folder = get_or_create_folder()
    counter = 1

    thread = start_keyboard_listener()
    detect = YOLODetection((1280, 1280))

    Storage()['lightning_started'] = True
    while Storage()['lightning_started']:
        img = detect.take_screenshot('cs2.exe')
        resized_image, _, _ = detect.resize_image(img, (640, 640))
        cv2.imwrite(str(dataset_folder / f'{counter}_640.jpg'), resized_image)
        resized_image, _, _ = detect.resize_image(img, (1280, 1280))
        cv2.imwrite(str(dataset_folder / f'{counter}_1280.jpg'), resized_image)
        counter += 1
        sleep(0.5)

    thread.join()

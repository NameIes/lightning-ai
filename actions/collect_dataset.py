import os
import cv2
from mss import mss
from colorama import Fore, Style
from pathlib import Path
from pynput import keyboard
from threading import Thread
from time import sleep
from core.storage import Storage
from utils.capture import take_screenshot, resize_image


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
        Storage().set_data('lightning_started', False)


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

    sct = mss()
    dataset_folder = get_or_create_folder()
    counter = 1

    thread = start_keyboard_listener()

    Storage().set_data('lightning_started', True)
    while Storage().data['lightning_started']:
        img = take_screenshot(sct, 'cs2.exe')
        resized_image, _, _ = resize_image(img)
        cv2.imwrite(str(dataset_folder / f'{counter}.jpg'), resized_image)
        counter += 1
        sleep(0.5)

    thread.join()

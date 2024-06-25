import os
from colorama import Fore, Style
from core.storage import Storage
from core.gsi_server import GSIServerManager
from core.keyboard import KeyboardListener
from core.mouse import MouseListener
from core.detect import YOLODetection
from core.lightning import Lightning


def print_info() -> None:
    os.system('cls')
    print('{}Lightning AI started. Press {}Pause Break{} to stop.{}'.format(
        Fore.GREEN,
        Fore.YELLOW + Style.BRIGHT,
        Style.RESET_ALL + Fore.GREEN,
        Style.RESET_ALL
    ))


def start() -> None:
    print_info()

    data_storage = Storage()
    data_storage['lightning_started'] = True

    keyboard = KeyboardListener()
    keyboard.start()

    mouse = MouseListener()

    gsi_server = GSIServerManager(('localhost', 8003), 'MYTOKENHERE')
    gsi_server.start()

    detection = YOLODetection((1280, 1280), 'cs2.exe')
    lightning = Lightning(mouse, detection.screensize)
    mouse.start(lightning)

    while data_storage['lightning_started']:
        pass

    keyboard.stop()
    mouse.stop()
    gsi_server.stop()
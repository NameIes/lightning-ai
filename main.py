import os
import sys
import colorama
import cutie
import shutil
from time import sleep
from pathlib import Path
from string import ascii_letters, digits
from core.storage import Storage
from actions.start import start
from actions.collect_dataset import collect_dataset
from actions.prepare_dataset import prepare_dataset
from actions.train_model import train_model
from utils.steam import get_cs2_path, get_steam_path, get_gsi_config_path

colorama.init()


def check_lightning_ai() -> None:
    print(colorama.Fore.LIGHTBLUE_EX + 'Checking Lightning AI...' + colorama.Style.RESET_ALL)

    base_dir = Path(__file__).parent
    Storage()['base_dir'] = base_dir

    allowed_chars = ascii_letters + digits + '.:/\\-_ '
    for char in str(base_dir):
        if char not in allowed_chars:
            print(base_dir)
            print(colorama.Fore.RED + 'Path to Lightning AI contains invalid characters.' + \
                colorama.Style.RESET_ALL)
            print(colorama.Fore.LIGHTBLUE_EX + 'Allowed characters are: ' + colorama.Fore.LIGHTWHITE_EX + \
                ' '.join(allowed_chars) + colorama.Style.RESET_ALL)
            exit()

    if not (base_dir / 'models' / 'pretraining.pt').exists():
        print(colorama.Fore.RED + 'Lightning AI model not found.' + colorama.Style.RESET_ALL)
        print(colorama.Fore.LIGHTBLUE_EX + 'You can download it from ' + colorama.Fore.LIGHTWHITE_EX + \
            'https://lightning.ai' + colorama.Style.RESET_ALL)
        print(colorama.Fore.LIGHTBLUE_EX + 'Then place it in ' + colorama.Fore.YELLOW + \
            'models' + colorama.Fore.LIGHTBLUE_EX + ' folder.' + colorama.Style.RESET_ALL)
        exit()


def check_cs2() -> None:
    print(colorama.Fore.LIGHTBLUE_EX + 'Checking Counter Strike 2 exists...' + colorama.Style.RESET_ALL)

    try:
        steam = get_steam_path()
        if not steam.exists():
            raise OSError()
    except OSError:
        print(colorama.Fore.RED + 'Steam not found.' + colorama.Style.RESET_ALL)
        exit()

    try:
        cs2 = get_cs2_path()
        if not cs2.exists():
            raise FileNotFoundError()
    except FileNotFoundError:
        print(colorama.Fore.RED + 'Counter Strike 2 not found.' + colorama.Style.RESET_ALL)
        exit()


def check_gsi() -> None:
    print(colorama.Fore.LIGHTBLUE_EX + 'Checking GSI installed...' + colorama.Style.RESET_ALL)

    cs2_gsi = get_gsi_config_path()
    if not cs2_gsi.exists():
        cs2_gsi.parent.mkdir(parents=True, exist_ok=True)
    lightning_gsi = Storage().data['base_dir'] / 'config' / 'gamestate_integration_GSI.cfg'

    if not lightning_gsi.exists():
        print(colorama.Fore.RED + 'GSI config not found. Please reinstall Lightning AI.' + colorama.Style.RESET_ALL)
        exit()

    if cs2_gsi.read_text() != lightning_gsi.read_text():
        shutil.copy(lightning_gsi, cs2_gsi)


def print_checks_passed() -> None:
    print(colorama.Fore.GREEN + 'All checks passed. Starting...' + colorama.Style.RESET_ALL)
    sleep(1)
    os.system('cls')


def close() -> None:
    os.system('cls')
    exit()


def show_menu() -> None:
    menu_labels = [
        'Start',
        'Collect dataset for training',
        'Prepare dataset',
        'Train model',
        'Settings',
        'Exit',
    ]
    menu_functions = [
        start,
        collect_dataset,
        prepare_dataset,
        train_model,
        lambda: print('4'),
        close,
    ]

    while True:
        menu_functions[cutie.select(menu_labels)]()
        os.system('cls')


if __name__ == '__main__':
    check_lightning_ai()
    if '--checks-off' not in sys.argv:
        check_cs2()
        check_gsi()
    print_checks_passed()
    show_menu()

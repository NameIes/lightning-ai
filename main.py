import os
import sys
import colorama
import cutie
from time import sleep
from pathlib import Path
from string import ascii_letters, digits

colorama.init()


def check_lightning_ai():
    print(colorama.Fore.BLUE + 'Checking Lightning AI...' + colorama.Style.RESET_ALL)

    base_dir = Path(__file__).parent
    allowed_chars = ascii_letters + digits + '.:/\\-_ '
    for char in str(base_dir):
        if char not in allowed_chars:
            print(base_dir)
            print(colorama.Fore.RED + 'Path to Lightning AI contains invalid characters.' + \
                colorama.Style.RESET_ALL)
            print(colorama.Fore.BLUE + 'Allowed characters are: ' + colorama.Fore.LIGHTWHITE_EX + \
                ' '.join(allowed_chars) + colorama.Style.RESET_ALL)
            exit()

    if not (base_dir / 'models' / 'pretraining.pt').exists():
        print(colorama.Fore.RED + 'Lightning AI model not found.' + colorama.Style.RESET_ALL)
        print(colorama.Fore.BLUE + 'You can download it from ' + colorama.Fore.LIGHTWHITE_EX + \
            'https://lightning.ai' + colorama.Style.RESET_ALL)
        print(colorama.Fore.BLUE + 'Then place it in ' + colorama.Fore.YELLOW + \
            'models' + colorama.Fore.BLUE + ' folder.' + colorama.Style.RESET_ALL)
        exit()


def check_cs2():
    # Check if steam installed
    # Find steam path
    # Check if cs2 installed
    # Find cs2 path
    print(colorama.Fore.BLUE + 'Checking Counter Strike 2 exists...' + colorama.Style.RESET_ALL)
    sleep(1)


def check_gsi():
    # Add gsi to start arguments of cs2
    # Copy gsi to cs2 folder
    # Copy cs2 sensivity to config folder
    print(colorama.Fore.BLUE + 'Checking GSI installed...' + colorama.Style.RESET_ALL)
    sleep(1)


def print_checks_passed():
    print(colorama.Fore.GREEN + 'All checks passed. Starting...' + colorama.Style.RESET_ALL)
    sleep(1)
    os.system('cls')


def close():
    os.system('cls')
    exit()


def show_menu():
    menu_labels = [
        'Start',
        'Collect dataset for training',
        'Prepare dataset and train',
        'Settings',
        'Exit',
    ]
    menu_functions = [
        lambda: print('1'),
        lambda: print('2'),
        lambda: print('3'),
        lambda: print('4'),
        close,
    ]

    menu_functions[cutie.select(menu_labels)]()


if __name__ == '__main__':
    check_lightning_ai()
    check_cs2()
    check_gsi()
    print_checks_passed()
    show_menu()

import os
import cutie
from colorama import Fore, Style
from core.storage import Storage


def settings() -> None:
    go_back = False
    while not go_back:
        os.system('cls')
        aim_types = ['aimbot', 'triggerbot', 'aimbot+triggerbot', 'inuria']
        aim_prioritets = ['Head+Body', 'Head', 'Body']
        lines = [
            'Name of game process: {}'.format(
                Fore.YELLOW +
                Storage()['settings']['process_name'] +
                Style.RESET_ALL
            ),
            'Start window with YOLO detection: {}'.format(
                Fore.YELLOW +
                str(Storage()['settings']['show_yolo']) +
                Style.RESET_ALL
            ),
            'AIM Type: {}'.format(
                Fore.YELLOW +
                str(Storage()['settings']['aim_type']) +
                Style.RESET_ALL
            ),
            'AIM Max Distance: {}'.format(
                Fore.YELLOW +
                str(Storage()['settings']['aim_max_distance']) +
                Style.RESET_ALL
            ),
            'AIM Priority: {}'.format(
                Fore.YELLOW +
                str(Storage()['settings']['aim_priority']) +
                Style.RESET_ALL
            ),
            'AIM Delay: {}'.format(
                Fore.YELLOW +
                str(Storage()['settings']['aim_delay']) +
                Style.RESET_ALL
            ),
            'Back to main menu'
        ]

        select_index = cutie.select(lines)
        if select_index == len(lines) - 1:
            go_back = True
        if select_index == 0:
            os.system('cls')
            Storage()['settings']['process_name'] = input('Name of game process: ' + Fore.YELLOW)
        if select_index == 1:
            Storage()['settings']['show_yolo'] = not Storage()['settings']['show_yolo']
        if select_index == 2:
            os.system('cls')
            Storage()['settings']['aim_type'] = aim_types[cutie.select(aim_types)]
        if select_index == 3:
            os.system('cls')
            Storage()['settings']['aim_max_distance'] = int(cutie.get_number('AIM Max Distance: ' + Fore.YELLOW))
        if select_index == 4:
            os.system('cls')
            Storage()['settings']['aim_priority'] = aim_prioritets[cutie.select(aim_prioritets)]
        if select_index == 5:
            os.system('cls')
            Storage()['settings']['aim_delay'] = int(cutie.get_number('AIM Delay: ' + Fore.YELLOW))
        print(Style.RESET_ALL)
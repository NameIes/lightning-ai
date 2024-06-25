from pynput import keyboard
from colorama import Fore, Style
from threading import Thread
from core.storage import Storage


class KeyboardListener:
    def __init__(self) -> None:
        self._thread = None

    def on_press(self, key) -> None:
        st = Storage()
        if key == keyboard.Key.pause:
            st['lightning_started'] = False
        if key == keyboard.Key.f8:
            if st['team'] == 'off':
                st['team'] = 'ct'
            elif st['team'] == 'ct':
                st['team'] = 't'
            elif st['team'] == 't':
                st['team'] = 'all'
            elif st['team'] == 'all':
                st['team'] = 'off'

            print(Fore.GREEN + 'Team: ' + st['team'] + Style.RESET_ALL)

    def start(self) -> Thread:
        listener = keyboard.Listener(on_press=self.on_press)
        self.thread = Thread(target=listener.start)
        self.thread.start()

    def stop(self) -> None:
        self.thread.join()

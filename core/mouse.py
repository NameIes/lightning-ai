import win32api, win32con
from pynput import mouse


class MouseListener:
    def __init__(self) -> None:
        self._thread = None
        self._lightning = None

    def on_click(self, x, y, button, pressed) -> None:
        if button == mouse.Button.left and not pressed:
            print('Left btn pressed')

    def start(self, lightning) -> None:
        self._lightning = lightning
        self.thread = mouse.Listener(on_click=self.on_click)
        self.thread.start()

    def move_mouse(x, y):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)

    def mouse_click():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

    def stop(self) -> None:
        self.thread.stop()
        self.thread.join()

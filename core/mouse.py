import win32con
import win32gui
import win32api

from ctypes import WINFUNCTYPE, c_int, Structure, cast, POINTER, windll
from ctypes.wintypes import LPARAM, WPARAM, DWORD, PULONG, LONG
from threading import Thread
from core.storage import Storage


def genStruct(name="Structure", **kwargs):
    return type(name, (Structure,), dict(
        _fields_=list(kwargs.items()),
        __str__=lambda self: "%s(%s)" % (name, ",".join("%s=%s" % (k, getattr(self, k)) for k in kwargs))
    ))


HookStruct = genStruct(
    "Hook", pt=genStruct("Point", x=LONG, y=LONG), mouseData=DWORD, flags=DWORD, time=DWORD, dwExtraInfo=PULONG)


@WINFUNCTYPE(LPARAM, c_int, WPARAM, LPARAM)
def hookProc(nCode, wParam, lParam):
    if wParam == win32con.WM_LBUTTONDOWN and Storage()['lightning_started']:
        msg = cast(lParam, POINTER(HookStruct))[0]
        if msg.flags == 0:
            th = Thread(target=Storage()['__on_click'])
            th.start()
            return 1
    return windll.user32.CallNextHookEx(None, nCode, WPARAM(wParam), LPARAM(lParam))


class MouseListener:
    def __init__(self) -> None:
        self._thread = None
        self._lightning = None
        self._click_function = lambda: None

    def __on_click(self) -> None:
        self._click_function()
        self.click()

    def _start(self) -> None:
        self.hook = windll.user32.SetWindowsHookExW(win32con.WH_MOUSE_LL, hookProc, None, 0)
        while Storage()['lightning_started']:
            win32gui.PumpWaitingMessages()

    def start(self, lightning) -> None:
        self._lightning = lightning
        Storage()['__on_click'] = self.__on_click
        self._thread = Thread(target=self._start)
        self._thread.start()

    def move(self, x, y):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)

    def click(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,1,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,1,0)

    def stop(self) -> None:
        Storage()['lightning_started'] = False
        if self.hook:
            windll.user32.UnhookWindowsHookEx(self.hook)
        Storage()['__on_click'] = None
        self._thread.join()
        print('Mouse listener stopped.')

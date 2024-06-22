import win32api, win32con
from time import sleep

def move_mouse(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)


def mouse_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

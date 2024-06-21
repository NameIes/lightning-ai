import win32gui
import win32process
import psutil
import ctypes
import ctypes.wintypes


EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
IsWindowVisible = ctypes.windll.user32.IsWindowVisible


def get_pid_by_name(process_name: str) -> list[int]:
    pids = []

    for proc in psutil.process_iter():
        if process_name in proc.name():
            pids.append(proc.pid)

    return pids


def get_hwnds_for_pid(pid: int) -> list[int]:
    def callback(hwnd, hwnds):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)

        if found_pid == pid:
            hwnds.append(hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds


def get_rect_by_hwnd(hwnd: int) -> dict:
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))

    return {
        'top': rect.top,
        'left': rect.left,
        'width': rect.right - rect.left,
        'height': rect.bottom - rect.top,
    }


def get_rect_by_name(process_name: str = 'cs2.exe') -> dict:
    pids = get_pid_by_name(process_name)

    for pid in pids:
        hwnds = get_hwnds_for_pid(pid)

        for hwnd in hwnds:
            if IsWindowVisible(hwnd):
                return get_rect_by_hwnd(hwnd)

    raise Exception('No window found.')

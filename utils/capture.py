import cv2
import numpy as np
from utils.window_box import get_rect_by_name
from mss.base import MSSBase


def take_screenshot(sct: MSSBase, process_name: str) -> cv2.typing.MatLike:
    box = get_rect_by_name(process_name)
    sct_img = sct.grab(box)
    img = np.array(sct_img)

    return img


def resize_image(img: cv2.typing.MatLike, size: tuple) -> tuple[cv2.typing.MatLike, tuple, tuple]:
    height, width = img.shape[:2]
    # if width >= height:
    #     new_width = 640
    #     new_height = int((640 / width) * height)
    # else:
    #     new_height = 640
    #     new_width = int((640 / height) * width)
    new_width = size[0]
    new_height = size[0]
    resized_image = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    if resized_image.shape[2] == 4:
        resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGRA2BGR)

    return resized_image, (width, height), (new_width, new_height)

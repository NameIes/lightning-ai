import numpy as np
import cv2
from PIL import Image
from mss import mss
from utils.window_box import get_rect_by_name


if __name__ == '__main__':
    sct = mss()
    while True:
        box = get_rect_by_name('Code.exe')
        sct_img = sct.grab(box)

        img = np.array(sct_img)
        res = cv2.resize(img, (960, 540), interpolation=cv2.INTER_CUBIC)

        cv2.imshow('screen', res)

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break

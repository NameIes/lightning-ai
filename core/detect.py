import cv2
import numpy as np
from mss import mss
from typing import Optional
from ultralytics import YOLO
from core.storage import Storage
from core.rect import Rect
from utils.window_box import get_rect_by_name


class YOLODetection:
    def __init__(self, img_size: tuple, process_name: str) -> None:
        self._model = YOLO(Storage()['base_dir'] / 'models' / 'best.pt')
        self._model.to('cuda')
        self._sct = mss()
        self._img_size = img_size
        self._process_name = process_name

        import ctypes
        user32 = ctypes.windll.user32
        self.screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    def take_screenshot(self) -> cv2.typing.MatLike:
        box = get_rect_by_name(self._process_name)
        sct_img = self._sct.grab(box)
        img = np.array(sct_img)

        return img

    def resize_image(self, img: cv2.typing.MatLike, size: tuple = None) -> tuple[cv2.typing.MatLike, tuple]:
        if size is None:
            size = self._img_size

        height, width = img.shape[:2]
        new_width = size[0]
        new_height = size[1]
        resized_image = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        if resized_image.shape[2] == 4:
            resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGRA2BGR)

        return resized_image, (width, height)

    def take_resized_screenshot(self, size: tuple = None) -> tuple[cv2.typing.MatLike, tuple]:
        if size is None:
            size = self._img_size
        img = self.take_screenshot(self._sct, self._process_name)
        return self.resize_image(img, size)

    def _transform_YOLO_boxes(self, boxes: Optional[np.array], orig_size: tuple, new_size: tuple) -> list[int, int, int, int, float, int]:
        orig_width, orig_height = orig_size
        new_width, new_height = new_size
        scale_x = orig_width / new_width
        scale_y = orig_height / new_height

        transformed_boxes = []
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            conflidense, class_id = box.conf[0], box.cls[0]
            x1 = int(x1 * scale_x)
            x2 = int(x2 * scale_x)
            y1 = int(y1 * scale_y)
            y2 = int(y2 * scale_y)
            transformed_boxes.append(Rect(x1, y1, x2, y2, conflidense, class_id))

        return transformed_boxes

    def predict(self, img: cv2.typing.MatLike, img_size: tuple) -> list:
        # ct - 1
        # ct_head - 2
        # t - 3
        # t_head - 4
        results = self._model(img, imgsz=self._img_size, verbose=False)[0]

        boxes = results.boxes.cpu().numpy()
        return self._transform_YOLO_boxes(boxes, img_size, self._img_size)

    def show_results(self, boxes: list[Rect], img: cv2.typing.MatLike) -> None:
        for box in boxes:
            x1 = box.x1
            y1 = box.y1
            x2 = box.x2
            y2 = box.y2
            conflidense = box.conf
            class_id = box.cls
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f'{class_id}: {conflidense:.2f}'
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('screen', img)
        cv2.waitKey(1)

    def stop(self) -> None:
        cv2.destroyAllWindows()

from time import sleep
from core.mouse import MouseListener
from core.rect import Rect
from core.storage import Storage


class Lightning:
    def __init__(self, mouse: MouseListener) -> None:
        self._st = Storage()
        self._mouse = mouse

    def vector_length(self, x1: int, y1: int, x2: int, y2: int) -> float:
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def is_cursor_in_rect(self, cur, rect):
        return cur[0] >= rect.x1 and cur[0] <= rect.x2 and cur[1] >= rect.y1 and cur[1] <= rect.y2

    # ct - 1
    # ct_head - 2
    # t - 3
    # t_head - 4

    def get_heads(self, boxes) -> list[Rect]:
        rects = []
        class_id = []
        if self._st['team'] == 'all':
            class_id = [2, 4]
        elif self._st['team'] == 'ct':
            class_id = [4]
        elif self._st['team'] == 't':
            class_id = [2]

        for box in boxes:
            if int(box[5]) in class_id:
                rects.append(Rect(box[0], box[1], box[2], box[3], box[4], box[5]))

        return rects

    def get_bodies(self, boxes) -> list[Rect]:
        rects = []
        class_id = []
        if self._st['team'] == 'all':
            class_id = [1, 3]
        elif self._st['team'] == 'ct':
            class_id = [1]
        elif self._st['team'] == 't':
            class_id = [3]

        for box in boxes:
            if int(box[5]) in class_id:
                rects.append(Rect(box[0], box[1], box[2], box[3], box[4], box[5]))

        return rects

    def aimbot(self, boxes, orig_size):
        if self._st['settings']['aim_priority'] == 'Head':
            heads = self.get_heads(boxes)
            if len(heads) > 0:
                boxes = heads
        if self._st['settings']['aim_priority'] == 'Body':
            bodies = self.get_bodies(boxes)
            if len(bodies) > 0:
                boxes = bodies

        if not boxes:
            return

        cur = (orig_size[0] // 2, orig_size[1] // 2)
        near_rect = boxes[0]
        distance = self.vector_length(cur[0], cur[1], near_rect.get_center()[0], near_rect.get_center()[1])

        for box in boxes:
            tmp_distance = self.vector_length(cur[0], cur[1], box.get_center()[0], box.get_center()[1])
            if tmp_distance < distance:
                distance = tmp_distance
                near_rect = box

        if int(distance) > self._st['settings']['aim_max_distance']:
            return

        x_shift = near_rect.get_center()[0] - cur[0]
        y_shift = near_rect.get_center()[1] - cur[1]
        self._mouse.move(x_shift, y_shift)

    def triggerbot(self, boxes, orig_size):
        cur = (orig_size[0] // 2, orig_size[1] // 2)
        for box in boxes:
            if self.is_cursor_in_rect(cur, box):
                if self._st['settings']['aim_delay'] > 0:
                    sleep(self._st['settings']['aim_delay'] / 1000)
                self._mouse.click()

    def inuria(self, boxes, orig_size) -> None:
        self.aimbot(boxes, orig_size)

    def process(self, boxes, orig_size) -> None:
        if self._st['team'] == 'off':
            return

        aim_type = self._st['settings']['aim_type']

        if aim_type == 'aimbot':
            self.aimbot(boxes, orig_size)

        if aim_type == 'triggerbot':
            self.triggerbot(boxes, orig_size)

        if aim_type == 'aimbot+triggerbot':
            self.aimbot(boxes, orig_size)
            self.triggerbot(boxes, orig_size)

        if aim_type == 'inuria':
            self._mouse._click_function = lambda: self.inuria(boxes, orig_size)

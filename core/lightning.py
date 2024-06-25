from time import sleep
from core.mouse import MouseListener
from core.rect import Rect
from core.storage import Storage


class Lightning:
    def __init__(self, mouse: MouseListener, screensize: tuple) -> None:
        self._st = Storage()
        self._mouse = mouse
        self.screen_size = screensize

    def vector_length(x1: int, y1: int, x2: int, y2: int) -> float:
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def is_cursor_in_rect(cur, rect):
        return cur[0] >= rect.x1 and cur[0] <= rect.x2 and cur[1] >= rect.y1 and cur[1] <= rect.y2

    # ct - 1
    # ct_head - 2
    # t - 3
    # t_head - 4

    def get_heads(self, boxes) -> list[Rect]:
        rects = []
        class_id = []
        if self._st.data['team'] == 'all':
            class_id = [2, 4]
        elif self._st.data['team'] == 'ct':
            class_id = [4]
        elif self._st.data['team'] == 't':
            class_id = [2]

        for box in boxes:
            if int(box[5]) in class_id:
                rects.append(Rect(box[0], box[1], box[2], box[3], box[4], box[5]))

        return rects

    def get_bodies(self, boxes) -> list[Rect]:
        rects = []
        class_id = []
        if self._st.data['team'] == 'all':
            class_id = [1, 3]
        elif self._st.data['team'] == 'ct':
            class_id = [1]
        elif self._st.data['team'] == 't':
            class_id = [3]

        for box in boxes:
            if int(box[5]) in class_id:
                rects.append(Rect(box[0], box[1], box[2], box[3], box[4], box[5]))

        return rects

    def aimbot(self, boxes):
        if self._st.data['aimbot_priority'] == 'Head':
            heads = self.get_heads(boxes)
            if len(heads) > 0:
                boxes = heads
        if self._st.data['aimbot_priority'] == 'Body':
            bodies = self.get_bodies(boxes)
            if len(bodies) > 0:
                boxes = bodies

        cur = (self.screen_size[0] // 2, self.screen_size[1] // 2)
        near_rect = min(boxes, key=lambda x: self.vector_length(cur[0], cur[1], x.get_center()[0], x.get_center()[1]))

        distance = self.vector_length(cur[0], cur[1], near_rect.get_center()[0], near_rect.get_center()[1])
        if int(distance) > self._st.data['aim_max_distance']:
            return

        x_shift = near_rect.get_center()[0] - cur[0]
        y_shift = near_rect.get_center()[1] - cur[1]
        self._mouse.move(x_shift, y_shift)

    def triggerbot(self, boxes):
        cur = (self.screen_size[0] // 2, self.screen_size[1] // 2)
        for box in boxes:
            if self.is_cursor_in_rect(cur, box):
                if self._st.data['aim_delay'] > 0:
                    sleep(self._st.data['aim_delay'] / 1000)
                self._mouse.click()

    def inuria(self, boxes):
        self.aimbot(boxes)

    def process(self, boxes) -> None:
        if self._st.data['team'] == 'off':
            return

        aim_type = self._st.data['aim_type']

        if aim_type == 'aimbot':
            self.aimbot(boxes)

        if aim_type == 'triggerbot':
            self.triggerbot(boxes)

        if aim_type == 'aimbot+triggerbot':
            self.aimbot(boxes)
            self.triggerbot(boxes)

        if aim_type == 'inuria':
            self._mouse._click_function = lambda: self.inuria(boxes)

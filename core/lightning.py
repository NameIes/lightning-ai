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
        if self._st.data['team'] == 'off':
            return []

        rects = []
        class_id = 2 if self._st.data['team'] == 't' else 4
        for box in boxes:
            if int(box[5]) == class_id:
                rects.append(Rect(box[0], box[1], box[2], box[3], box[4], box[5]))

        return rects

    def get_bodies(self, boxes) -> list[Rect]:
        if self._st.data['team'] == 'off':
            return []

        rects = []
        class_id = 1 if self._st.data['team'] == 't' else 3
        for box in boxes:
            if int(box[5]) == class_id:
                rects.append(Rect(box[0], box[1], box[2], box[3], box[4], box[5]))

        return rects

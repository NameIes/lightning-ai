class Rect:
    def __init__(self, x1, y1, x2, y2, conf, cls):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.conf = conf
        self.cls = cls

    def get_center(self):
        return (int((self.x1 + self.x2) / 2), int((self.y1 + self.y2) / 2))

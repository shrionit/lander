class CollisionBox:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.left = pos.x - size.x / 2
        self.right = pos.x + size.x / 2
        self.top = pos.y - size.y / 2
        self.bottom = pos.y + size.y / 2

    def collidesWith(self, box):
        hc = False
        vc = False
        if box.left < self.right or box.right > self.left:
            hc = True
        if box.top < self.bottom or box.bottom > self.top:
            vc = True
        return hc and vc


class CollisionBoxGroup:
    def __init__(self, boxes: [CollisionBox]):
        self.boxes = boxes

    def collidesWith(self, box):
        out = False
        for b in self.boxes:
            if b.collidesWith(box):
                out = True
                break
        return out

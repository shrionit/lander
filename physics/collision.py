class CollisionBox:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.left = pos.x
        self.right = pos.x + size.x
        self.top = pos.y
        self.bottom = pos.y + size.y

    def collidesWith(self, box):
        vy = box.velocity.y
        vx = box.velocity.x
        collided = False
        if self.left <= box.bounds.right + vx and self.right >= box.bounds.left - vx:
            if self.top < box.bounds.bottom + vy:# and self.left <= box.bounds.right + vx and self.right >= box.bounds.left - vx and self.bottom >= box.bounds.top + vy:
                box.pos.y = self.top - box.size.y
                box.velocity.y = 0
                collided = True
        return collided


class CollisionBoxGroup:
    def __init__(self, boxes: [CollisionBox]):
        self.boxes = boxes

    def collidesWith(self, box):
        out = None
        for b in self.boxes:
            out = b.collidesWith(box)
            if out:
                break
        return out

from math import fabs
from core.utils import Dict


class CollisionBox:
    def __init__(self, pos, size):
        self.dir = Dict(
            left=False,
            right=False,
            top=False,
            bottom=False
        )
        self.pos = pos
        self.size = size
        self.left = pos.x
        self.right = pos.x + size.x
        self.top = pos.y
        self.bottom = pos.y + size.y

    def collidesWith(self, box):
        vy = box.velocity.y
        vx = box.velocity.x
        self.dir.left = self.left < box.bounds.right + vx
        self.dir.right = self.right > box.bounds.left - vx
        self.dir.top = self.top < box.bounds.bottom + vy
        self.dir.bottom = self.bottom > box.bounds.top - vy
        xcoll = self.dir.left and self.dir.right
        ycoll = self.dir.top and self.dir.bottom
        if xcoll and self.dir.top:
            box.velocity.y = 0
        if xcoll and self.dir.bottom:
            box.velocity.y *= -1
        return self if xcoll and ycoll else False


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

import glfw
import json, os

import glm
import numpy as np

from physics.collision import CollisionBox, CollisionBoxGroup


class Dict(dict):
    """
    Dict (dict_object):
        Makes a dictionay object act as javascript object

    Example:
        person = Dict({
            'id': 1,
            'name': 'John'
        })

        person.id = 2

        print(person.id) # 2
    """

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


def getTime():
    return np.float32(glfw.get_time())


def getHeightWithRatio(w, a, b):
    """ Returns height for given width 'w' with ratio a:b """
    return b * w // a


def loadJSON(filepath):
    path = os.getcwd() + "\\assets\\" + filepath
    file = open(path)
    data = json.load(file)
    file.close()
    return data


def getTexOffsetFromIndex(imageWidth, imageHeight, tileWidth, tileHeight, index):
    n_tile = imageWidth // tileWidth
    y = index // n_tile
    x = index % n_tile
    x *= tileWidth
    y *= tileHeight
    return np.round(x / imageWidth, 8), np.round(y / imageHeight, 8)


def getTexCoordsFromIndex(imageWidth, imageHeight, tileWidth, tileHeight, index):
    n_tile = imageWidth // tileWidth
    y = index // n_tile
    x = index % n_tile
    xoff = tileWidth / imageWidth
    yoff = tileHeight / imageHeight
    left = (x * tileWidth) / imageWidth
    bottom = (y * tileHeight) / imageHeight
    right = ((x + 1) * tileWidth) / imageWidth
    top = ((y + 1) * tileHeight) / imageHeight
    # left = xoff * x
    # bottom = yoff * y
    # right = left + xoff
    # top = bottom + yoff
    return [
        left, bottom,
        right, bottom,
        right, top,
        left, top
    ]


def getCollisionBoxes(tiles):
    out = Dict()
    for tile in tiles:
        collision_boxes = []
        for colbox in tile['objectgroup']['objects']:
            colbox = Dict(colbox)
            collision_boxes.append(
                CollisionBox(glm.vec2(colbox.x, colbox.y), glm.vec2(colbox.width, colbox.height))
            )
        out[tile['id']] = CollisionBoxGroup(collision_boxes)
    return out

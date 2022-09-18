import glfw
import numpy as np


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

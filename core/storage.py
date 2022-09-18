import numpy as np
from OpenGL.GL import *


class BufferObject:
    def __init__(self, buffer, type, drawtype) -> None:
        self.buffer = buffer
        self.type = type
        self.drawtype = drawtype
        self.itemCount = 0

    def bind(self):
        glBindBuffer(self.type, self.buffer)

    def unbind(self):
        glBindBuffer(self.type, 0)

    def data(self, data):
        self.itemCount = len(data)
        glBufferData(self.type, data, self.drawtype)

    def __del__(self):
        self.unbind()
        glDeleteBuffers(1, [self.buffer])


class VBO(BufferObject):
    def __init__(self, data=None, draw_type=GL_STATIC_DRAW) -> None:
        self.buffer = glGenBuffers(1)
        super().__init__(self.buffer, GL_ARRAY_BUFFER, draw_type)
        self.auto(data)

    def auto(self, data):
        if data is not None:
            self.bind()
            self.data(np.array(data, dtype=np.float32))
            self.unbind()


class IBO(BufferObject):
    def __init__(self, data=None) -> None:
        self.buffer = glGenBuffers(1)
        super().__init__(self.buffer, GL_ELEMENT_ARRAY_BUFFER, GL_STATIC_DRAW)
        self.auto(data)

    def auto(self, data):
        if data is not None:
            self.bind()
            self.data(np.array(data, dtype=np.int32))
            self.unbind()


class VAO:
    VAOS = []
    def __init__(self) -> None:
        self.buffer = glGenVertexArrays(1)
        self.hasIndices = False
        self.indicesCount = 0
        self.vertexCount = 0

    def loadBufferToAttribLocation(
        self,
        attrNum,
        bufferObject,
        ddim=3,
        dtype=GL_FLOAT,
        normalized=GL_FALSE,
        stride=0,
        pointer=None,
        per_instance=False
    ):
        self.bind()
        bufferObject.bind()
        if attrNum == 0: self.vertexCount = bufferObject.itemCount / 3
        glEnableVertexAttribArray(attrNum)
        glVertexAttribPointer(attrNum, ddim, dtype, normalized, stride * 4, pointer if pointer is None else pointer * 4)
        if per_instance:
            glVertexAttribDivisor(attrNum, 1)
        self.unbind()
        del bufferObject

    def loadIndices(self, bufferObject):
        self.bind()
        bufferObject.bind()
        self.hasIndices = True
        self.indicesCount = bufferObject.itemCount
        self.unbind()
        del bufferObject

    def bind(self):
        glBindVertexArray(self.buffer)

    def unbind(self):
        glBindVertexArray(0)

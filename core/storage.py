import ctypes

import numpy as np
from OpenGL.GL import *


class BufferObject:
    BOS = []

    def __init__(self, buffer, type, drawtype) -> None:
        self.buffer = buffer
        BufferObject.BOS.append(self.buffer)
        self.type = type
        self.drawtype = drawtype
        self.itemCount = 0

    def bind(self):
        glBindBuffer(self.type, self.buffer)

    def unbind(self):
        glBindBuffer(self.type, 0)

    def data(self, size=None, data=None, usage=GL_STATIC_DRAW):
        self.itemCount = len(data)
        glBufferData(self.type, size=size, data=data, usage=self.drawtype)

    @staticmethod
    def cleanup():
        glDeleteBuffers(len(BufferObject.BOS), BufferObject.BOS)

    def __del__(self):
        glDeleteBuffers(1, [self.buffer])


class VBO(BufferObject):
    def __init__(
        self, data=None, buffer=None, buffer_size=3, draw_type=GL_STATIC_DRAW
    ) -> None:
        self.bufferSize = buffer_size * 4
        self.buffer = buffer or glGenBuffers(1)
        super().__init__(self.buffer, GL_ARRAY_BUFFER, draw_type)
        self.auto(data)

    def auto(self, data):
        if data is not None:
            self.bind()
            self.data(data=np.array(data, dtype=np.float32))
            self.unbind()

    def update(self, data):
        self.bind()
        glBufferData(GL_ARRAY_BUFFER, size=self.bufferSize, usage=self.drawtype)
        glBufferSubData(GL_ARRAY_BUFFER, 0, data=np.array(data, dtype=np.float32))
        self.unbind()

    @staticmethod
    def empty(size, draw_type=GL_STATIC_DRAW):
        vbo = VBO(draw_type=draw_type, buffer_size=size)
        vbo.bind()
        glBufferData(GL_ARRAY_BUFFER, vbo.bufferSize, usage=draw_type)
        vbo.unbind()
        return vbo


class IBO(BufferObject):
    def __init__(self, data=None) -> None:
        self.buffer = glGenBuffers(1)
        super().__init__(self.buffer, GL_ELEMENT_ARRAY_BUFFER, GL_STATIC_DRAW)
        self.auto(data)

    def auto(self, data):
        if data is not None:
            self.bind()
            self.data(data=np.array(data, dtype=np.int32))
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
        offset=0,
    ):
        self.bind()
        bufferObject.bind()
        if attrNum == 0:
            self.vertexCount = bufferObject.itemCount / ddim
        glEnableVertexAttribArray(attrNum)
        glVertexAttribPointer(
            attrNum,
            ddim,
            dtype,
            normalized,
            stride * 4,
            ctypes.c_void_p(offset),
        )
        self.unbind()
        del bufferObject

    def loadInstanceBufferToAttribLocation(
        self,
        attrNum,
        vbo,
        ddim=3,
        dtype=GL_FLOAT,
        normalized=GL_FALSE,
        instanceDataLength=0,
        offset=0,
    ):
        self.bind()
        vbo.bind()
        glEnableVertexAttribArray(attrNum)
        glVertexAttribPointer(
            attrNum,
            ddim,
            dtype,
            normalized,
            instanceDataLength,
            ctypes.c_void_p(offset),
        )
        glVertexAttribDivisor(attrNum, 1)
        vbo.unbind()
        self.unbind()

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

    @staticmethod
    def cleanup():
        glDeleteVertexArrays(len(VAO.VAOS), VAO.VAOS)

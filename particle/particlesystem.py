import numpy as np
import glm
from OpenGL.GL import *

import gmath
from camera import Camera
from core import shapes
from core.renderer import Renderer
from core.shader import Shader
from core.shapes import RECT
from core.storage import VAO, IBO, VBO
from core.texture import Texture
from entity import Entity
from gmath import createTransformationMatrix, randomVec3


class ParticleShader(Shader):
    DEFAULT_NAME = "particleShader"

    def __init__(self, name=DEFAULT_NAME, frag=None, vert=None):
        if not (frag and vert):
            super().__init__(frag=name, vert=name)
        else:
            super().__init__(frag=frag, vert=vert)


class Particle(Entity):

    def __init__(self, position, rotation=glm.vec3(0), scale=glm.vec3(1), model=RECT, texture: Texture = None,
                 shader: Shader = None):
        self.model = model
        self.vao = VAO()
        self._setupModel()
        super().__init__(position, rotation, scale, self.vao, texture, shader)

    def _setupModel(self):
        self.vao.loadBufferToAttribLocation(0, VBO(self.model.vertices))
        self.vao.loadBufferToAttribLocation(1, VBO(self.model.texCoords), ddim=2)
        self.vao.loadIndices(IBO(self.model.indices))

    def getTransformationMatrix(self):
        return createTransformationMatrix(self.position, self.rotation, self.scale)

    def update(self, shader: Shader = None):
        shader = shader or self.shader
        if shader is not None:
            shader.loadTransformationMatrix(self.getTransformationMatrix())

    def render(self, shader: Shader = None):
        shader = shader or self.shader
        shader.attach()
        self.update(shader)
        self.texture.bind()
        self.vao.bind()
        glDrawElements(GL_TRIANGLES, self.vao.indicesCount, GL_UNSIGNED_INT, None)
        self.vao.unbind()
        self.texture.unbind()
        shader.detach()


class ParticleSystem(Renderer):
    MAX_INSTANCES = 10000

    def __init__(self, particle: Particle, count=1, shader: Shader = None, camera: Camera = None):
        self.particle = particle
        self.shader = shader
        self.count = count
        self.camera = camera

        self.vbo = VBO(buffer_size=ParticleSystem.MAX_INSTANCES * 4, draw_type=GL_STREAM_DRAW)
        self.vbo.update(self._getRandomVec3Arr())
        self.particle.vao.bind()
        self.particle.vao.loadInstanceBufferToAttribLocation(2, self.vbo)
        self.particle.vao.unbind()

    def _getRandomVec3Arr(self):
        return np.array([randomVec3(-5, 5) for _ in range(self.count)], np.float32)

    def update(self):
        self.camera.update(self.shader)
        self.particle.update(self.shader)

    def render(self):
        self.update()
        self.shader.attach()
        self.particle.texture.bind()
        self.particle.bind()
        glDrawElementsInstanced(GL_TRIANGLES, self.particle.vao.indicesCount, GL_UNSIGNED_INT, None, self.count)
        self.particle.unbind()
        self.particle.texture.bind()
        self.shader.detach()

    def cleanup(self):
        del self.vbo

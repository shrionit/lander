import random
from copy import copy
import numpy as np
import glm
from OpenGL.GL import *
import gmath
from camera import Camera
from core import shapes
from core.display import Window
from core.renderer import Renderer
from core.shader import Shader
from core.shapes import RECT
from core.storage import VAO, IBO, VBO
from core.texture import Texture
from gmath import createTransformationMatrix, randomVec3
from physics import base


class ParticleShader(Shader):
    DEFAULT_NAME = "particleShader"

    def __init__(self, name=DEFAULT_NAME, frag=None, vert=None):
        if not (frag and vert):
            super().__init__(frag=name, vert=name)
        else:
            super().__init__(frag=frag, vert=vert)


class Particle:
    def __init__(
            self,
            position,
            rotation: float = 0,
            scale: float = 1,
            vao: VAO = None,
            model=RECT,
            gravityEffect: float = 0,
            vel: glm.vec3 = glm.vec3(0),
            acc: glm.vec3 = glm.vec3(0),
            mass: float = 1,
            life: float = 1,
    ):
        self.life = life
        self.elapsedTime = 0
        self.gravityEffect = gravityEffect
        self.oldPos = glm.vec3(position)
        self.oldVel = glm.vec3(vel)
        self.oldAcc = glm.vec3(acc)
        self.position = position
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)
        self.vel = vel
        self.acc = acc
        self.mass = mass
        if vao is None:
            self.model = model
            self.vao = VAO()
            self._setupModel()
        else:
            self.vao = vao

    def _setupModel(self):
        self.vao.loadBufferToAttribLocation(0, VBO(self.model.vertices))
        self.vao.loadBufferToAttribLocation(1, VBO(self.model.texCoords), ddim=2)
        self.vao.loadIndices(IBO(self.model.indices))

    def isAlive(self):
        return self.life > self.elapsedTime

    def getTransformationMatrix(self):
        return createTransformationMatrix(self.position, self.rotation, self.scale)

    def update(self):
        if self.isAlive():
            force = self.acc / self.mass
            force.y += base.GRAVITY * self.gravityEffect * Window.get_deltatime()
            self.vel *= Window.get_deltatime()
            self.vel += force
            self.position += self.vel
            self.elapsedTime += Window.get_deltatime()
            return
        self.position = glm.vec3(self.oldPos)
        self.vel = glm.vec3(self.oldVel)
        self.acc = glm.vec3(self.oldAcc)
        self.elapsedTime = 0

    def bind(self):
        self.vao.bind()

    def unbind(self):
        self.vao.unbind()


class ParticleSystem(Renderer):
    MAX_INSTANCES = 10000

    def __init__(
            self,
            origins: any,
            texture: Texture,
            count: int = 1,
            shader: Shader = None,
            camera: Camera = None,
    ):
        self.origins = origins
        self.texture = texture
        self.shader = shader
        self.count = count
        self.camera = camera
        self.vao = VAO()
        self.particles = [None] * self.count * len(self.origins)
        for i in range(len(self.particles)):
            self.particles[i] = Particle(
                position=glm.vec3(self.origins[i // self.count]),
                life=random.random() * 1,
                gravityEffect=0.1,
                vao=self.vao,
                mass=2,
                scale=0.1,
                vel=glm.vec3(0, 0, 0),
                acc=randomVec3(-0.01, 0.01),
            )
        self.vbo = VBO(
            buffer_size=ParticleSystem.MAX_INSTANCES * 16, draw_type=GL_STREAM_DRAW
        )
        m = self.getParticlesTransformations()
        self.vbo.update(m)
        self.vao.bind()
        self.vao.loadBufferToAttribLocation(0, VBO(RECT.vertices))
        self.vao.loadBufferToAttribLocation(1, VBO(RECT.texCoords), ddim=2)
        self.vao.loadInstanceBufferToAttribLocation(
            2, self.vbo, ddim=4, instanceDataLength=16 * 4, offset=0
        )
        self.vao.loadInstanceBufferToAttribLocation(
            3, self.vbo, ddim=4, instanceDataLength=16 * 4, offset=16
        )
        self.vao.loadInstanceBufferToAttribLocation(
            4, self.vbo, ddim=4, instanceDataLength=16 * 4, offset=32
        )
        self.vao.loadInstanceBufferToAttribLocation(
            5, self.vbo, ddim=4, instanceDataLength=16 * 4, offset=48
        )
        self.vao.loadIndices(IBO(RECT.indices))
        self.vao.unbind()

    def getParticlesTransformations(self):
        out = []
        for particle in self.particles:
            out.extend(particle.getTransformationMatrix())
        return np.array(out, np.float32)

    def update(self):
        self.camera.update(self.shader)
        for particle in self.particles:
            particle.update()
        self.vbo.update(self.getParticlesTransformations())

    def start(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthMask(GL_FALSE)
        self.shader.attach()
        self.texture.bind()
        self.vao.bind()

    def stop(self):
        glDisable(GL_BLEND)
        glDepthMask(True)
        self.vao.unbind()
        self.texture.unbind()
        self.shader.detach()

    def render(self):
        self.update()
        self.start()
        glDrawElementsInstanced(
            GL_TRIANGLES,
            self.vao.indicesCount,
            GL_UNSIGNED_INT,
            None,
            self.count * len(self.origins),
        )
        self.stop()

    def cleanup(self):
        del self.vbo

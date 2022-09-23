import glm

from camera import Camera
from core.shader import Shader
from core.shapes import RECT
from core.storage import BufferObject, VAO, VBO, IBO
from core.texture import Texture
from entity import Entity
from particle.particlesystem import ParticleSystem, Particle, ParticleShader


class Scene:

    def __init__(self, window):
        self.shader = Shader(frag='basic', vert='basic')
        self.texture = Texture("test.jpg")
        self.camera = Camera(window, glm.vec3(0.0, 0.0, 5.0), glm.vec3(0.0, 1.0, 0.0))
        self.particles = ParticleSystem(
            Particle(glm.vec3(1, 1, -1), texture=self.texture),
            camera=self.camera,
            shader=ParticleShader(name="particleShader"),
            count=2
        )
        self.entity = None

    def setup(self):
        vao = VAO()
        vao.loadBufferToAttribLocation(0, VBO(RECT.vertices))
        vao.loadBufferToAttribLocation(1, VBO(RECT.texCoords), ddim=2)
        vao.loadIndices(IBO(RECT.indices))
        self.entity = Entity(vao=vao, shader=self.shader, texture=self.texture)

    def render(self):
        self.shader.attach()
        self.camera.update(self.shader)
        self.entity.bind()
        self.entity.render()
        self.entity.unbind()
        self.shader.detach()
        self.particles.render()

    def cleanup(self):
        self.particles.cleanup()
        BufferObject.cleanup()
        VAO.cleanup()

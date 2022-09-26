import glm
from OpenGL.GL import glDrawElements, GL_TRIANGLES, GL_UNSIGNED_INT

from camera import Camera
from core.framebuffer import FrameBuffer
from core.shader import Shader
from core.shapes import RECT
from core.storage import BufferObject, VAO, VBO, IBO
from core.texture import Texture
from entity import Entity
from particle.particlesystem import ParticleSystem, Particle, ParticleShader


class Scene:

    def __init__(self, window):
        self.sceneShader = Shader(name='sceneShader')
        self.shader = Shader(frag='basic', vert='basic')

        # FBO to render the scene
        self.fbo = FrameBuffer(window.WIDTH, window.HEIGHT)
        self.texture = Texture(texID=self.fbo.getFB().textureId)

        # SCREEN VAO
        self.screen = VAO()
        self.screen.loadBufferToAttribLocation(0, VBO([e*2 for e in RECT.vertices]))
        self.screen.loadBufferToAttribLocation(1, VBO(RECT.texCoords), ddim=2)
        self.screen.loadIndices(IBO(RECT.indices))

        self.camera = Camera(window, glm.vec3(0.0, 0.0, 5.0), glm.vec3(0.0, 1.0, 0.0))
        self.particles = ParticleSystem(
            origins=[
                glm.vec3(1),
                glm.vec3(0)
            ],
            texture=Texture("particle.png"),
            camera=self.camera,
            shader=ParticleShader(name="particleShader"),
            count=500
        )
        self.entity = None

    def setup(self):
        vao = VAO()
        vao.loadBufferToAttribLocation(0, VBO(RECT.vertices))
        vao.loadBufferToAttribLocation(1, VBO(RECT.texCoords), ddim=2)
        vao.loadIndices(IBO(RECT.indices))
        self.entity = Entity(vao=vao, shader=self.shader, texture=Texture("test.jpg"))

    def render(self, fbo: FrameBuffer = None):
        self.shader.attach()
        self.camera.update(self.shader)
        self.entity.bind()
        self.entity.render()
        self.entity.unbind()
        self.shader.detach()
        self.particles.render()

    def renderScene(self):
        self.render(self.fbo)
        self.sceneShader.attach()
        self.texture.bind()
        self.screen.bind()
        glDrawElements(GL_TRIANGLES, self.screen.indicesCount, GL_UNSIGNED_INT, None)
        self.screen.unbind()
        self.texture.unbind()
        self.sceneShader.detach()


    def cleanup(self):
        self.particles.cleanup()
        BufferObject.cleanup()
        VAO.cleanup()

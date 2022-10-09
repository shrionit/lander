import glfw
import glm
from OpenGL.GL import *

from Camera2D import Camera2D
from core.display import Window
from core.input import is_key_pressed
from camera import Camera
from core.framebuffer import Framebuffer
from core.postprocessing import PostProcessor, EFFECTS
from core.shader import Shader
from core.shapes import RECT
from core.storage import BufferObject, VAO, VBO, IBO
from core.texture import Texture
from core.utils import getHeightWithRatio
from entity import Entity
from level.level import Level
from lightsystem import LightSystem
from particle.particlesystem import ParticleSystem, Particle, ParticleShader


class Scene:
    def __init__(self, window):
        self.sceneShader = Shader(name="sceneShader")
        self.shader = Shader(frag="basic", vert="basic")
        self.window = window
        # FBO to render the scene
        self.fbo = Framebuffer(self.window.WIDTH, self.window.HEIGHT, multiSample=False)
        self.screenTexture = Texture(texID=self.fbo.textureID, dim=(self.window.WIDTH, self.window.HEIGHT))
        # SCREEN VAO
        self.screen = VAO()
        self.screen.loadBufferToAttribLocation(0, VBO([e * 2 for e in RECT.vertices]))
        self.screen.loadBufferToAttribLocation(1, VBO(RECT.texCoords), ddim=2)
        self.screen.loadIndices(IBO(RECT.indices))
        # Post Processor
        self.fx = PostProcessor(self.screen)
        self.camera = Camera2D(position=glm.vec3(0, 0, -5))
        # Light System
        self.lightsystem = LightSystem(self.screen, Texture(textures="test.jpg"), self.camera)
        self.lightsystem.addLight(glm.vec3(5, 5, 0), glm.vec4(1, 0, 0, 1))
        self.level = Level("level0.tmj", camera=self.camera)

    def setup(self):
        self.camera.update(self.shader)
        vao = VAO()
        vao.loadBufferToAttribLocation(0, VBO(RECT.vertices))
        vao.loadBufferToAttribLocation(1, VBO(RECT.texCoords), ddim=2)
        vao.loadIndices(IBO(RECT.indices))


    def render(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glCullFace(GL_FRONT)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw
        self.level.draw()

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)

    def renderScene(self):
        self.fbo.bind()
        self.render()
        self.fbo.unbind()
        self.fx.applyEffect(EFFECTS.EDGE, self.fbo)
        self.fx.applyEffect(EFFECTS.BLUR, self.fbo)
        self.lightsystem.render()
        self.screenTexture.bind()
        self.sceneShader.attach()
        self.screen.bind()
        glDrawElements(GL_TRIANGLES, self.screen.indicesCount, GL_UNSIGNED_INT, None)
        self.screen.unbind()
        self.sceneShader.detach()
        self.screenTexture.unbind()

    def cleanup(self):
        self.level.cleanup()
        BufferObject.cleanup()
        Framebuffer.cleanUP()
        VAO.cleanup()

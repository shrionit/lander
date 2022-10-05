import glfw
import glm
from OpenGL.GL import *

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
from particle.particlesystem import ParticleSystem, Particle, ParticleShader


class Scene:
    def __init__(self, window):
        self.sceneShader = Shader(name="sceneShader")
        self.shader = Shader(frag="basic", vert="basic")
        self.window = window
        # FBO to render the scene
        self.fbo = Framebuffer(self.window.WIDTH, self.window.HEIGHT, multiSample=False)
        self.screenTexture = Texture(texID=self.fbo.textureID)
        # SCREEN VAO
        self.screen = VAO()
        self.screen.loadBufferToAttribLocation(0, VBO([e * 2 for e in RECT.vertices]))
        self.screen.loadBufferToAttribLocation(1, VBO(RECT.texCoords), ddim=2)
        self.screen.loadIndices(IBO(RECT.indices))
        # Post Processor
        self.fx = PostProcessor(self.screen)

        self.camera = Camera(self.window, glm.vec3(0.0, 0.0, -0.001), glm.vec3(0.0, 1.0, 0.0))
        self.particles = ParticleSystem(
            origins=[glm.vec3(1), glm.vec3(0)],
            texture=Texture("particle.png"),
            camera=self.camera,
            shader=ParticleShader(name="particleShader"),
            count=500,
        )
        self.entities = None

    def setup(self):
        self.camera.update(self.shader)
        vao = VAO()
        vao.loadBufferToAttribLocation(0, VBO(RECT.vertices))
        vao.loadBufferToAttribLocation(1, VBO(RECT.texCoords), ddim=2)
        vao.loadIndices(IBO(RECT.indices))
        self.entities = [
            # Entity(
            #     vao=vao,
            #     shader=self.shader,
            #     position=glm.vec3(0, 0, -1.5),
            #     scale=glm.vec3(8, getHeightWithRatio(8, 16, 9), 0.0),
            #     texture=Texture("Cave\\background.png"),
            #     texMovementMult=0.1,
            # ),
            # Entity(
            #     vao=vao,
            #     shader=self.shader,
            #     position=glm.vec3(0, 0, -1.0),
            #     scale=glm.vec3(4, getHeightWithRatio(4, 16, 9), 0.0),
            #     texture=Texture("Cave\\back-walls.png"),
            #     texMovementMult=0.05,
            # ),
            # Entity(
            #     vao=vao,
            #     shader=self.shader,
            #     position=glm.vec3(0, 0, -0.1),
            #     scale=glm.vec3(2, getHeightWithRatio(2, 16, 9), 0.0),
            #     texture=Texture("Cave\\tiles.png"),
            #     texMovementMult=.001,
            # ),
            Entity(
                vao=vao,
                shader=self.shader,
                texture=Texture("test.jpg"),
                texMovementMult=0,
                position=glm.vec3(0),
                scale=glm.vec3(.1)
            ),
        ]
        tex = self.entities[-1].texture
        # xmin = getHeightWithRatio(16, 16, 9)
        for y in range(-5, 6):
            for x in range(-7, 8):
                self.entities.append(
                    Entity(
                        vao=vao,
                        shader=self.shader,
                        texture=tex,
                        texMovementMult=0,
                        position=glm.vec3(x, y, 0.0),
                        scale=glm.vec3()
                    )
                )

    def render(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glCullFace(GL_FRONT)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.shader.attach()
        self.camera.update(self.shader)
        for entity in self.entities:
            entity.bind()
            if is_key_pressed(glfw.KEY_RIGHT):
                self.shader.setUniform1("offsetX", entity.getRightTexOffset().x)
            if is_key_pressed(glfw.KEY_LEFT):
                self.shader.setUniform1("offsetX", entity.getLeftTexOffset().x)
            entity.render()
            entity.unbind()
        self.shader.detach()
        # self.particles.render()
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)

    def renderScene(self):
        self.fbo.bind()
        self.render()
        self.fbo.unbind()
        # self.fx.applyEffect(EFFECTS.EDGE, self.fbo)
        # self.fx.applyEffect(EFFECTS.BLUR, self.fbo)
        self.screenTexture.bind()
        self.sceneShader.attach()
        self.screen.bind()
        glDrawElements(GL_TRIANGLES, self.screen.indicesCount, GL_UNSIGNED_INT, None)
        self.screen.unbind()
        self.sceneShader.detach()
        self.screenTexture.unbind()

    def cleanup(self):
        self.particles.cleanup()
        BufferObject.cleanup()
        Framebuffer.cleanUP()
        VAO.cleanup()

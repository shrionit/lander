import glm
from OpenGL.GL import glDrawElements
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_TRIANGLES, GL_UNSIGNED_INT

from Camera2D import Camera2D
from core.framebuffer import Framebuffer
from core.input import mouse
from core.shader import Shader
from core.texture import Texture
from gmath import createTransformationMatrix


class LightShader(Shader):
    DEFAULT_NAME = "lightShader"

    def __init__(self, name=DEFAULT_NAME, frag=None, vert=None):
        if not (frag and vert):
            super().__init__(frag=name, vert=name)
        else:
            super().__init__(frag=frag, vert=vert)


class Light:
    def __init__(self, pos: glm.vec3 = glm.vec3(0), color: glm.vec4 = glm.vec4(1)):
        self.pos = pos
        self.color = color

    def getTransformationMatrix(self):
        return createTransformationMatrix(self.pos, glm.vec3(0), glm.vec3(1))

    def setPos(self, pos):
        self.pos = pos


class LightSystem:
    def __init__(self, quadVAO, fbo: Framebuffer, camera: Camera2D):
        self.vao = quadVAO
        self.fbo = fbo
        self.shader = LightShader()
        self.camera = camera
        self.lights = []

    def addLight(self, pos, color: glm.vec4 = glm.vec4(1)):
        self.lights.append(Light(pos, color))

    def update(self, shader: Shader = None):
        shader = shader or self.shader
        self.camera.update(shader)

    def start(self):
        self.shader.attach()
        self.vao.bind()
        self.fbo.bind()
        Texture.bindTexture(self.fbo.textureID)

    def stop(self):
        self.vao.unbind()
        Texture.bindTexture(0)
        self.fbo.unbind()
        self.shader.detach()

    def render(self):
        self.start()
        self.update()
        for i in range(len(self.lights)):
            self.lights[i].setPos(glm.vec3(mouse.x, mouse.y, 0))
            self.shader.setUniformVec3(f"lights[{i}].position", self.lights[i].pos.to_list())
            self.shader.setUniformVec4(f"lights[{i}].color", self.lights[i].color.to_list())
            self.shader.loadTransformationMatrix(self.lights[i].getTransformationMatrix())
            glDrawElements(GL_TRIANGLES, self.vao.indicesCount, GL_UNSIGNED_INT, None)
        self.stop()


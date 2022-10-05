import glm
from OpenGL.GL import *
from core.shader import Shader
from core.shapes import RECT
from core.storage import VAO, VBO, IBO
from core.texture import Texture
from core.utils import Dict
from gmath import createTransformationMatrix


class SpriteShader(Shader):
    DEFAULT_NAME = "spriteShader"

    def __init__(self, name=DEFAULT_NAME, frag=None, vert=None):
        if not (frag and vert):
            super().__init__(frag=name, vert=name)
        else:
            super().__init__(frag=frag, vert=vert)

    def setTexOffset(self, offset: glm.vec2 = glm.vec2(0)):
        self.setUniformVec2("texOffset", offset)


class Sprite:
    def __init__(
            self,
            pos: glm.vec3 = glm.vec3(0),
            size: glm.vec2 = glm.vec2(1),
            rotate: float = 0,
            tex: Texture = None,
            shader: Shader = None,
            elapsedFrame: int = 0,
            frameBuffer: int = 2,
            frameSize: int = 64,
            frameCount: int = 1
    ):
        self.shader = shader
        self.pos = pos
        self.size = size
        self.rotate = rotate
        self.tex = tex
        self.loop = False
        self.elapsedFrame = elapsedFrame
        self.frameBuffer = frameBuffer
        self.frameSize = frameSize
        self.frameCount = frameCount
        self.bounds = Dict()
        self.calculateBounds()
        data = [
            0.0, 1.0, 0.0, 1.0,
            1.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 
    
            0.0, 1.0, 0.0, 1.0,
            1.0, 1.0, 1.0, 1.0,
            1.0, 0.0, 1.0, 0.0
        ]
        
        self.vao = VAO()
        self.vao.loadBufferToAttribLocation(0, VBO(data), ddim=4)

    def calculateBounds(self):
        self.bounds.left = self.pos.x - self.size.x / 2
        self.bounds.right = self.pos.x + self.size.x / 2
        self.bounds.bottom = self.pos.y - self.size.y / 2
        self.bounds.top = self.pos.y + self.size.y / 2

    def getTransformationMatrix(self):
        return createTransformationMatrix(self.pos, glm.vec3(0, 0, self.rotate), glm.vec3(self.size, 0))

    def update(self, shader: Shader = None):
        shader = shader or self.shader
        if shader is not None:
            shader.loadTransformationMatrix(self.getTransformationMatrix())

    def render(self):
        self.tex.bind()
        self.vao.bind()
        # glDrawElements(GL_TRIANGLES, self.vao.indicesCount, GL_UNSIGNED_INT, None)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        self.vao.unbind()
        self.tex.unbind()


class SpriteRenderer:

    def __init__(self, shader: SpriteShader = None):
        self.shader = shader or SpriteShader()
        self.sprites = []

    def process(self, sprites = []):
        self.sprites = sprites

    def renderSprites(self, shader=None):
        shader = shader or self.shader
        shader.attach()
        for sprite in self.sprites:
            sprite.update(shader)
            sprite.render()
        shader.detach()

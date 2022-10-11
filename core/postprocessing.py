from OpenGL.GL import *
from core.shader import Shader
from core.texture import Texture
from core.framebuffer import Framebuffer
from core.utils import Dict

EFFECTS = Dict({
    "BLUR": [
        1.0 / 16, 2.0 / 16, 1.0 / 16,
        2.0 / 16, 4.0 / 16, 2.0 / 16,
        1.0 / 16, 2.0 / 16, 1.0 / 16
    ],
    "EDGE": [
        1, 1, 1,
        1, -8, 1,
        1, 1, 1
    ],
    "SHARP": [
        -1, -1, -1,
        -1, 1, -1,
        -1, -1, -1
    ]
})


class FXShader(Shader):
    DEFAULT_NAME = "fxshader"

    def __init__(self, name=DEFAULT_NAME, frag=None, vert=None):
        if not (frag and vert):
            super().__init__(frag=name, vert=name)
        else:
            super().__init__(frag=frag, vert=vert)

    def loadKernel(self, kernel):
        for i in range(len(kernel)):
            self.setUniform1(f"kernel[{i}]", kernel[i])


class PostProcessor:

    def __init__(self, quadVAO):
        self.vao = quadVAO
        self.bloom = 1
        self.shader = FXShader()
        self.blur = 0

    def applyEffect(self, effect: EFFECTS, fbo: Framebuffer) -> Texture:
        fbo.bind()
        self.shader.attach()
        self.shader.loadKernel(effect)
        Texture.bindTexture(fbo.textureID)
        self.vao.bind()
        glDrawElements(GL_TRIANGLES, self.vao.indicesCount, GL_UNSIGNED_INT, None)
        self.vao.unbind()
        self.shader.detach()
        fbo.unbind()
        return Texture(texID=fbo.textureID)

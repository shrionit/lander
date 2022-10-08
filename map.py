import numpy as np
import glm
from OpenGL.GL import *

from core.shader import Shader
from core.shapes import RECT
from core.storage import VAO, VBO, IBO
from core.texture import Texture
from core.utils import Dict, loadJSON
from sprite import Sprite, SpriteShader

WORLD_BOUNDS = Dict()
WORLD_BOUNDS.LEFT = 0
WORLD_BOUNDS.RIGHT = 64 * 30
WORLD_BOUNDS.TOP = 0
WORLD_BOUNDS.BOTTOM = 64 * 20


class Map:

    def __init__(self, texture: Texture, tileWidth: int = 64, tileHeight: int = 64):
        self.texture = texture
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.shader = Shader(frag="mapShader", vert="mapShader")
        self.tiles = []
        self.generateMapSprites()
        self.vao = VAO()
        self.vboTransforms = VBO(
            buffer_size=30 * 20 * 16
        )
        self.vboTexCoords = VBO(
            buffer_size=30 * 20 * 16
        )
        self.vboTransforms.update(self.getTilesTransformations())
        self.vboTexCoords.update(self.getTileTexCoords())
        self.vao.bind()
        self.vao.loadBufferToAttribLocation(0, VBO(RECT.CENTERED.vertices))
        self.vao.loadInstanceBufferToAttribLocation(
            1, self.vboTexCoords, ddim=2, instanceDataLength=8*4, offset=0
        )
        self.vao.loadInstanceBufferToAttribLocation(
            2, self.vboTransforms, ddim=4, instanceDataLength=16 * 4, offset=0
        )
        self.vao.loadInstanceBufferToAttribLocation(
            3, self.vboTransforms, ddim=4, instanceDataLength=16 * 4, offset=16
        )
        self.vao.loadInstanceBufferToAttribLocation(
            4, self.vboTransforms, ddim=4, instanceDataLength=16 * 4, offset=32
        )
        self.vao.loadInstanceBufferToAttribLocation(
            5, self.vboTransforms, ddim=4, instanceDataLength=16 * 4, offset=48
        )
        self.vao.loadIndices(IBO(RECT.indices))
        self.vao.unbind()

    def getTilesTransformations(self):
        out = []
        for tile in self.tiles:
            out.extend(tile.getTransformationMatrix())
        return np.array(out, np.float32)

    def getTileTexCoords(self):
        out = []
        for tile in self.tiles:
            out.extend(tile.getTexCoords())
        return np.array(out, np.float32)

    def generateMapSprites(self):
        level = loadJSON("levels\\level0.json")
        self.tiles = []
        for y in range(WORLD_BOUNDS.BOTTOM // 64):
            for x in range(WORLD_BOUNDS.RIGHT // 64):
                i = x + y * WORLD_BOUNDS.RIGHT // 64
                self.tiles.append(
                    Sprite(
                        pos=glm.vec3(x * 64, y * 64, 5.0),
                        size=glm.vec2(64),
                        texMapSize=self.texture.dim,
                        tileSize=(self.tileWidth, self.tileHeight),
                        tileIndex=level[i]
                    )
                )
        return self.tiles

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
        self.start()
        glDrawElementsInstanced(
            GL_TRIANGLES,
            self.vao.indicesCount,
            GL_UNSIGNED_INT,
            None,
            len(self.tiles),
        )
        self.stop()

    def cleanup(self):
        del self.vboTransforms
        del self.vboTexCoords

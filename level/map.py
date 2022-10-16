import numpy as np
import glm
from OpenGL.GL import *

from constants import WORLD_TILE_SIZE, WORLD_BOUNDS
from core.shader import Shader
from core.shapes import RECT
from core.storage import VAO, VBO, IBO
from core.texture import Texture
from physics.collision import CollisionBox, CollisionBoxGroup
from sprite import Sprite


class Map:

    def __init__(self, texture: Texture, level = None, shader: Shader = None, tileWidth: int = WORLD_TILE_SIZE, tileHeight: int = WORLD_TILE_SIZE):
        self.texture = texture
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.shader = shader or Shader(frag="mapShader", vert="mapShader")
        self.nTileWidth = tileWidth/self.texture.dim[0]
        self.nTileHeight = tileHeight/self.texture.dim[1]
        self.tileSize = glm.vec2(self.nTileWidth, self.nTileHeight).to_list()
        self.shader.attach()
        self.shader.setUniformVec2("tileSize", self.tileSize)
        self.shader.detach()
        self.tiles = []
        self.tilesTexOffsets = []
        self.tileTransforms = []
        self.generateMapSprites(level)
        self.vao = VAO()
        self.vboTransforms = VBO(
            buffer_size=30 * 20 * 16
        )
        self.vboTransforms.update(self.tileTransforms)
        self.vao.bind()
        self.vao.loadBufferToAttribLocation(0, VBO(RECT.CENTERED.vertices))
        # self.vao.loadBufferToAttribLocation(1, VBO(RECT.CENTERED.texCoords), ddim=2)
        self.vao.loadInstanceBufferToAttribLocation(
            1, VBO(self.tilesTexOffsets), ddim=2, instanceDataLength=2 * 4, offset=0
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
        self.vao.loadIndices(IBO(RECT.CENTERED.indices))
        self.vao.unbind()

    def getTilesTransformations(self):
        out = []
        for tile in self.tiles:
            out.extend(tile.getTransformationMatrix())
        return np.array(out, np.float32)

    def getTileTexCoords(self):
        out = []
        for tile in self.tiles:
            out.extend([tile.getTexCoords()])
        return np.array(out, np.float32)

    def generateMapSprites(self, level):
        self.tiles = []
        self.tilesTexOffsets = []
        self.tileTransforms = []
        for y in range(WORLD_BOUNDS.BOTTOM // WORLD_TILE_SIZE):
            for x in range(WORLD_BOUNDS.RIGHT // WORLD_TILE_SIZE):
                i = x + y * WORLD_BOUNDS.RIGHT // WORLD_TILE_SIZE
                if level[i] > 0:
                    sprite = Sprite(
                        pos=glm.vec3(x * WORLD_TILE_SIZE, y * WORLD_TILE_SIZE, 5.0),
                        size=glm.vec2(WORLD_TILE_SIZE),
                        texMapSize=self.texture.dim,
                        tileSize=(self.tileWidth, self.tileHeight),
                        tileIndex=level[i] - 1
                    )
                    if i==129:
                        print(level[i])
                    self.tilesTexOffsets.extend(sprite.getTexOffset())
                    self.tileTransforms.extend(sprite.getTransformationMatrix())
                    self.tiles.append(sprite)
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

class CollisionMap:

    def __init__(self, collisionsBoxes, groundMap):
        self.collisionBoxGroups = []
        for tile in groundMap.tiles:
            boxes = collisionsBoxes.get(tile.tileIndex)
            if boxes is None: continue
            coll_boxes = []
            for box in boxes:
                factor = glm.vec2(
                    tile.size.x / tile.tileSize[0],
                    tile.size.y / tile.tileSize[1]
                )
                coll_boxes.append(
                    CollisionBox(pos=tile.pos, size=glm.vec2(box.width*factor.x, box.height*factor.y))
                )
            self.collisionBoxGroups.append(
                CollisionBoxGroup(coll_boxes)
            )

    def getCollisionBoxGroups(self):
        return self.collisionBoxGroups


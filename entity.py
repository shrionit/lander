import glm
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_NEAREST

from core.display import Window
from core.input import KEYS, is_key_pressed
from core.shader import Shader
from core.texture import Texture
from core.utils import Dict
from constants import WORLD_BOUNDS, WORLD_TILE_SIZE
from sprite import Sprite


class Entity(Sprite):
    def __init__(
            self,
            position: glm.vec3 = glm.vec3(0),
            rotation: float = 0,
            size: glm.vec2 = glm.vec2(64),
            texture: Texture = None,
            shader: Shader = None,
            loop: bool = False,
            elapsedFrame: int = 0,
            frameBuffer: int = 2,
            frameSize: int = 64,
            frameCount: int = 1,
            static: bool = False,
            noPhysics: bool = False,
            texMapSize=(Window.WIDTH, Window.HEIGHT),
            tileSize=(64, 64),
            tileIndex=0,
    ) -> None:
        super().__init__(
            pos=position,
            size=size,
            rotate=rotation,
            shader=shader,
            loop=loop,
            tex=texture,
            elapsedFrame=elapsedFrame,
            frameBuffer=frameBuffer,
            frameSize=frameSize,
            frameCount=frameCount,
            texMapSize=texMapSize,
            tileSize=tileSize,
            tileIndex=tileIndex,
        )
        self.touchedGround = False
        self.currentTile = Dict(x=0, y=0)
        self.direction = 1
        self.moveSpeed = 50
        self.collidedPlateform = Dict(top=0)
        self.static = static
        self.noPhysics = noPhysics
        self.jumpHeight = 75
        self.velocity = glm.vec3(0, 0, 0)
        self.pressedTime = 0
        self.gravity = 2.9
        self.acceleration = glm.vec3(0, self.gravity, 0)
        self.idleSprite = Dict(
            right=Texture(assets="playerSheets\\IdleRight.png", filter=GL_NEAREST),
            left=Texture(assets="playerSheets\\IdleLeft.png", filter=GL_NEAREST),
        )
        self.runSprite = Dict(
            right=Texture(assets="playerSheets\\RunRight.png", filter=GL_NEAREST),
            left=Texture(assets="playerSheets\\RunLeft.png", filter=GL_NEAREST),
        )
        self.jumpSprite = Dict(
            right=Texture(assets="playerSheets\\JumpRight.png", filter=GL_NEAREST),
            left=Texture(assets="playerSheets\\JumpLeft.png", filter=GL_NEAREST),
        )
        self.level = None

    def setLevel(self, level):
        self.level = level

    def getCurrentTile(self):
        return f"{self.currentTile.x}-{self.currentTile.y}"

    def updatePos(self):
        self.pos += self.velocity
        self.calculateBounds()
        self.currentTile.x = int(self.pos.x // WORLD_TILE_SIZE)
        self.currentTile.y = int(self.pos.y // WORLD_TILE_SIZE)
        if self.currentTile.x < 0: self.currentTile.x = 0


    def checkCollision(self):
        if not self.level:
            return
        out = False
        self.currentTile.y += 1
        print(f"currentTile: {self.currentTile}")
        group = self.level.collisionMap.getCollisionBoxGroups().get(self.getCurrentTile())
        print(f"group: {group}")
        if group is None: return False
        out = group.collidesWith(self)
        # print(self.level.collisionMap.getCollisionBoxGroups().get(self.currentTile))
        # for group in self.level.collisionMap.getCollisionBoxGroups().values():
        #     out = out or group.collidesWith(self)
        return out

    def applyPhysics(self):
        self.updatePos()
        topBound = self.bounds.top + self.velocity.y > WORLD_BOUNDS.TOP
        bottomBound = self.bounds.bottom + self.velocity.y < WORLD_BOUNDS.BOTTOM
        collided = self.checkCollision()
        if not collided:
            if bottomBound:
                if not topBound:
                    self.velocity.y = 0
                self.velocity += self.acceleration * Window.get_deltatime()
            else:
                self.velocity.y = 0
        else:
            self.touchedGround = True
            self.collidedPlateform = collided

    def handleMovement(self):
        if is_key_pressed(KEYS.SPACE) and self.touchedGround and self.bounds.bottom > self.collidedPlateform.top - self.jumpHeight:
            self.setTexture(
                self.jumpSprite.left if self.direction == -1 else self.jumpSprite.right,
                self.tileSize,
            )
            self.velocity.y -= Window.get_deltatime() * 10
        if (
                is_key_pressed(KEYS.A)
                and self.bounds.left - self.velocity.x > WORLD_BOUNDS.LEFT
        ):
            self.direction = -1
            self.setTexture(self.runSprite.left, self.tileSize)
            self.elapsedFrame += Window.get_deltatime() * self.animationSpeed * 5.5
            self.velocity.x = -self.moveSpeed * Window.get_deltatime()
        elif (
                is_key_pressed(KEYS.D)
                and self.bounds.right + self.velocity.x < WORLD_BOUNDS.RIGHT
        ):
            self.direction = 1
            self.setTexture(self.runSprite.right, self.tileSize)
            self.elapsedFrame += Window.get_deltatime() * self.animationSpeed * 5.5
            self.velocity.x = self.moveSpeed * Window.get_deltatime()
        else:
            self.velocity.x = 0
            self.setTexture(
                self.idleSprite.left if self.direction == -1 else self.idleSprite.right,
                self.tileSize,
            )
        self.updatePos()

    def beforeRender(self):
        if not self.static:
            self.handleMovement()
            if not self.noPhysics:
                self.applyPhysics()

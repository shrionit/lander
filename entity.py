import glm
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_NEAREST

from core.display import Window
from core.input import KEYS, is_key_pressed
from core.shader import Shader
from core.texture import Texture
from level.map import WORLD_BOUNDS
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
            tileIndex=0
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
            tileIndex=tileIndex
        )
        self.moveSpeed = 100
        self.static = static
        self.noPhysics = noPhysics
        self.jumpForce = -1
        self.velocity = glm.vec3(0, 0, 0)
        self.gravity = 2.9
        self.acceleration = glm.vec3(0, self.gravity, 0)
        self.idleSprite = Texture(assets="playerSheets\\ChikBoy_idle.png", filter=GL_NEAREST)
        self.runSprite = Texture(assets="playerSheets\\ChikBoy_run.png", filter=GL_NEAREST)
        self.level = None

    def setLevel(self, level):
        self.level = level

    def updatePos(self):
        self.pos += self.velocity
        self.calculateBounds()

    def checkCollision(self):
        if not self.level: return
        # TODO: Collision

    def applyPhysics(self):
        self.updatePos()
        self.checkCollision()
        topBound = self.bounds.top + self.velocity.y > WORLD_BOUNDS.TOP
        bottomBound = self.bounds.bottom + self.velocity.y < WORLD_BOUNDS.BOTTOM
        if bottomBound:
            if not topBound:
                self.velocity.y = 0
            self.velocity += self.acceleration * Window.get_deltatime()
        else:
            self.velocity.y = 0

    def handleMovement(self):
        if is_key_pressed(KEYS.SPACE) and self.velocity.y == 0:
            self.velocity.y = self.jumpForce
        if is_key_pressed(KEYS.A) and self.bounds.left - self.velocity.x > WORLD_BOUNDS.LEFT:
            self.setTexture(self.runSprite, (-32, 32))
            self.velocity.x = -self.moveSpeed * Window.get_deltatime()
        elif is_key_pressed(KEYS.D) and self.bounds.right + self.velocity.x < WORLD_BOUNDS.RIGHT:
            self.setTexture(self.runSprite, (32, 32))
            self.velocity.x = self.moveSpeed * Window.get_deltatime()
        else:
            self.velocity.x = 0
            self.setTexture(self.idleSprite, (32, 32))
        self.updatePos()

    def beforeRender(self):
        if not self.static:
            self.handleMovement()
            if not self.noPhysics:
                self.applyPhysics()

from abc import abstractmethod
from logging import getLogger

import glm
from OpenGL.GL import glDrawElements, glDrawArrays, GL_TRIANGLES, GL_UNSIGNED_INT

from core.display import Window
from core.input import KEYS, is_key_pressed
from core.shader import Shader
from core.storage import VAO
from core.texture import Texture
from gmath import createTransformationMatrix
from map import WORLD_BOUNDS
from sprite import Sprite


class Entity(Sprite):
    def __init__(
            self,
            position: glm.vec3 = glm.vec3(0),
            rotation: float = 0,
            size: glm.vec2 = glm.vec2(64),
            texture: Texture = None,
            shader: Shader = None,
            texOffset: glm.vec2 = glm.vec2(0),
            texMovementMult: float = 1.0,
            elapsedFrame: int = 0,
            frameBuffer: int = 2,
            frameSize: int = 64,
            frameCount: int = 1,
            static: bool = False,
    ) -> None:
        super().__init__(
            pos=position,
            size=size,
            rotate=rotation,
            shader=shader,
            tex=texture,
            elapsedFrame=elapsedFrame,
            frameBuffer=frameBuffer,
            frameSize=frameSize,
            frameCount=frameCount,
        )
        self.moveSpeed = 1.0
        self.texMovementMult = texMovementMult
        self.texOffset = texOffset
        self.static = False
        self.jumpForce = -3
        self.velocity = glm.vec3(0, 0, 0)
        self.gravity = 0.98
        self.acceleration = glm.vec3(0, self.gravity / 100, 0)

    def applyPhysics(self):
        self.pos += self.velocity
        self.calculateBounds()
        topBound = self.bounds.top + self.velocity.y > WORLD_BOUNDS.TOP
        bottomBound = self.bounds.bottom + self.velocity.y < WORLD_BOUNDS.BOTTOM
        if bottomBound:
            if not topBound:
                self.velocity.y = 0
            self.velocity += self.acceleration
        else:
            self.velocity.y = 0

    def handleMovement(self):
        if is_key_pressed(KEYS.SPACE) and self.velocity.y == 0:
            self.velocity.y = self.jumpForce
        if is_key_pressed(KEYS.A) and self.bounds.left - self.velocity.x > WORLD_BOUNDS.LEFT:
            self.velocity.x = -self.moveSpeed
        elif is_key_pressed(KEYS.D) and self.bounds.right + self.velocity.x < WORLD_BOUNDS.RIGHT:
            self.velocity.x = self.moveSpeed
        else:
            self.velocity.x = 0

    def beforeRender(self):
        if not self.static:
            self.handleMovement()
            self.applyPhysics()

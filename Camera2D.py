import glm
from glfw import (
    KEY_W,
    KEY_A,
    KEY_S,
    KEY_D,
    KEY_UP,
    KEY_DOWN,
    KEY_LEFT,
    KEY_RIGHT,
    MOUSE_BUTTON_MIDDLE,
    KEY_LEFT_SHIFT,
    KEY_LEFT_CONTROL,
)
from OpenGL.GL import *

from core.display import Window
from core.input import is_key_pressed
from core.utils import Dict

YAW = -90.0
PITCH = 0.0
SPEED = 20.5
SENSITIVITY = 0.1
ZOOM = 45.0

Camera_Movement = Dict()
Camera_Movement.LEFT = KEY_A
Camera_Movement.RIGHT = KEY_D
Camera_Movement.UP = KEY_W
Camera_Movement.DOWN = KEY_S

class Camera2D:
    WORLD_LEFT = 0
    WORLD_RIGHT = 64*30
    WORLD_TOP = 0
    WORLD_BOTTOM = 64*20

    def __init__(self, position: glm.vec3 = glm.vec3(0)):
        self.playerTarget = None
        self.scale = 1
        self.aspectRatio = 0
        self.Position = position
        self.isFollowingPlayer = False
        self.Front = glm.vec3(0, 0, -1)
        self.Up = glm.vec3(0, 1, 0)
        self.Right = glm.vec3(1, 0, 0)
        self.MovementSpeed = SPEED
        self.MouseSensitivity = SENSITIVITY
        self.Zoom = ZOOM
        self.frameLeft = 0
        self.frameRight = 64*3
        self.frameTop = 0
        self.frameBottom = 64*2

    def GetViewMatrix(self) -> glm.mat4:
        return glm.lookAt(self.Position, self.Position + self.Front, self.Up)

    def GetProjectionMatrix(self) -> glm.mat4:
        # perspective = glm.perspective(glm.radians(self.Zoom), self.window.WIDTH / self.window.HEIGHT, 0.1, 100.0)
        """
        Maps
        (-1, 1)     (1, 1)

        (-1, -1)    (1, -1)
        To
        (0, 0)      (64*30, 0)

        (0, 64*20)  (64*30, -64*20)

        """
        ortho = glm.orthoLH(0, 64 * 30, 64*20, 0, 0.0, 1000)
        return ortho

    def Init(self, x, y, width, height):
        pass

    def update(self, shader):
        shader.attach()
        shader.loadProjectionMatrix(self.GetProjectionMatrix())
        shader.loadViewMatrix(self.GetViewMatrix())
        self.processKeyboard()

    def processKeyboard(self):
        speed = self.MovementSpeed * Window.get_deltatime()
        if is_key_pressed(Camera_Movement.UP):
            self.Position.y -= speed
        if is_key_pressed(Camera_Movement.DOWN):
            self.Position.y += speed
        if is_key_pressed(Camera_Movement.LEFT):
            self.Position.x -= speed
        if is_key_pressed(Camera_Movement.RIGHT):
            self.Position.x += speed


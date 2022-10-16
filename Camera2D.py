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
from core.input import is_key_pressed, mouse
from core.utils import Dict
from constants import WORLD_BOUNDS

YAW = -90.0
PITCH = 0.0
SPEED = 20.5
SENSITIVITY = 0.1
ZOOM = 1.0

Camera_Movement = Dict()
Camera_Movement.LEFT = KEY_A
Camera_Movement.RIGHT = KEY_D
Camera_Movement.UP = KEY_W
Camera_Movement.DOWN = KEY_S


class Camera2D:
    WORLD_LEFT = WORLD_BOUNDS.LEFT
    WORLD_RIGHT = WORLD_BOUNDS.RIGHT
    WORLD_TOP = WORLD_BOUNDS.TOP
    WORLD_BOTTOM = WORLD_BOUNDS.BOTTOM

    def __init__(self, position: glm.vec3 = glm.vec3(0), playerTarget=None):
        self.playerTarget = None
        self.Position = position
        self.isFollowingPlayer = False
        self.MovementSpeed = SPEED
        self.MouseSensitivity = SENSITIVITY
        self.Zoom = ZOOM
        self.frameLeft = 0
        self.frameRight = 64 * 3
        self.frameTop = 0
        self.frameBottom = 64 * 2
        self.viewRect = Dict()
        self.viewRect.width = WORLD_BOUNDS.RIGHT / 2
        self.viewRect.height = (WORLD_BOUNDS.BOTTOM / 2) * (16/9)
        self.viewRect.left = 0
        self.viewRect.right = 0
        self.viewRect.top = 0
        self.viewRect.bottom = 0

    def setTargetPlayer(self, player):
        self.playerTarget = player

    def GetViewMatrix(self) -> glm.mat4:
        m = glm.identity(glm.mat4)
        # m = glm.translate(m, self.playerTarget.pos)
        return m

    def calcViewRect(self, xoff=0, yoff=0):
        if xoff < 0 : xoff = 0
        if xoff+self.viewRect.width > WORLD_BOUNDS.RIGHT: xoff = WORLD_BOUNDS.RIGHT - self.viewRect.width
        if yoff < 0 : yoff = 0
        if yoff+self.viewRect.height > WORLD_BOUNDS.BOTTOM: yoff = WORLD_BOUNDS.BOTTOM - self.viewRect.height
        self.viewRect.left = xoff
        self.viewRect.right = xoff + self.viewRect.width
        self.viewRect.top = yoff
        self.viewRect.bottom = yoff + self.viewRect.height

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
        hViewTileCount = 30
        playerPos = self.playerTarget.pos
        xoff = playerPos.x - self.viewRect.width / 2
        yoff = playerPos.y - self.viewRect.height / 2
        self.calcViewRect(xoff, yoff)
        left = self.viewRect.left
        right = self.viewRect.right
        top = self.viewRect.top
        bottom = self.viewRect.bottom
        rect = [left, right, bottom, top]
        ortho = glm.orthoLH(*rect, 0.0, 1000)
        return ortho

    def Init(self, x, y, width, height):
        pass

    def update(self, shader):
        shader.attach()
        shader.loadProjectionMatrix(self.GetProjectionMatrix())
        shader.loadViewMatrix(self.GetViewMatrix())
        self.Zoom = 2 + mouse.scrollY * 0.01
        self.viewRect.width = WORLD_BOUNDS.RIGHT / self.Zoom
        self.viewRect.height = WORLD_BOUNDS.RIGHT / self.Zoom
        self.Zoom = 1
        # self.processKeyboard()

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

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
import glm
from core.shader import Shader
from core.utils import Dict
from OpenGL.GL import *
from gmath import *
from core.input import is_key_pressed, mouse, is_mouse_pressed, clear_mouse

# Defines several possible options for camera movement. Used as abstraction to stay away from window-system specific input methods
Camera_Movement = Dict()
Camera_Movement.FORWARD = KEY_W
Camera_Movement.BACKWARD = KEY_S
Camera_Movement.LEFT = KEY_A
Camera_Movement.RIGHT = KEY_D
Camera_Movement.UP = KEY_LEFT_SHIFT
Camera_Movement.DOWN = KEY_LEFT_CONTROL


# Default camera values
YAW = -90.0
PITCH = 0.0
SPEED = 2.5
SENSITIVITY = 0.1
ZOOM = 45.0


# An abstract camera class that processes input and calculates the corresponding Euler Angles, Vectors and Matrices for use in OpenGL
class Camera:
    def __init__(self, window, *args, **kwargs):
        if len(args) == 4 and len(kwargs) == 0:
            pos, up, yaw, pitch = args

            self.Position = pos
            self.WorldUp = up
            self.Yaw = yaw
            self.Pitch = pitch

        elif len(args) + len(kwargs) <= 4:
            keyword_arguments = ("position", "up", "yaw", "pitch")
            keyword_arguments_defaults = {
                "position": glm.vec3(),
                "up": glm.vec3(0, 1, 0),
                "yaw": YAW,
                "pitch": PITCH,
            }

            for i in range(len(args)):
                kw = keyword_arguments[i]
                value = args[i]
                kwargs[kw] = value

            keyword_arguments_defaults.update(kwargs)

            self.Position = keyword_arguments_defaults["position"]
            self.WorldUp = keyword_arguments_defaults["up"]
            self.Yaw = keyword_arguments_defaults["yaw"]
            self.Pitch = keyword_arguments_defaults["pitch"]

        else:
            raise TypeError("Invalid argument count for Camera()")

        self.Front = glm.vec3(0.0, 0.0, -1.0)
        self.Up = glm.vec3()
        self.Right = glm.vec3()
        self.MovementSpeed = SPEED
        self.MouseSensitivity = SENSITIVITY
        self.Zoom = ZOOM
        self.window = window

        self.updateCameraVectors()

    # returns the view matrix calculated using Euler Angles and the LookAt Matrix
    def GetViewMatrix(self) -> glm.mat4:
        return glm.lookAt(self.Position, self.Position + self.Front, self.Up)

    def GetProjectionMatrix(self) -> glm.mat4:
        return glm.perspective(glm.radians(self.Zoom), self.window.WIDTH / self.window.HEIGHT, 0.1, 100.0)

    def update(self, shader):
        shader.attach()
        shader.loadProjectionMatrix(self.GetProjectionMatrix())
        shader.loadViewMatrix(self.GetViewMatrix())
        self.ProcessKeyboard()
        self.ProcessMouseMovement(mouse.dx, mouse.dy, on_key=MOUSE_BUTTON_MIDDLE)
        self.ProcessMouseScroll(mouse.scrollY)
        clear_mouse()

    # processes input received from any keyboard-like input system. Accepts input parameter in the form of camera defined ENUM (to abstract it from windowing systems)
    def ProcessKeyboard(self) -> None:
        velocity = self.MovementSpeed * self.window.get_deltatime()
        if is_key_pressed(Camera_Movement.FORWARD):
            self.Position += self.Front * velocity
        if is_key_pressed(Camera_Movement.BACKWARD):
            self.Position -= self.Front * velocity
        if is_key_pressed(Camera_Movement.LEFT):
            self.Position -= self.Right * velocity
        if is_key_pressed(Camera_Movement.RIGHT):
            self.Position += self.Right * velocity
        if is_key_pressed(Camera_Movement.UP):
            self.Position += self.Up * velocity
        if is_key_pressed(Camera_Movement.DOWN):
            self.Position -= self.Up * velocity

    # processes input received from a mouse input system. Expects the offset value in both the x and y direction.
    def ProcessMouseMovement(
        self, xoffset: float, yoffset: float, constrainPitch: bool = True, on_key=None
    ) -> None:
        if on_key is not None and not is_mouse_pressed(MOUSE_BUTTON_MIDDLE): return
        
        xoffset *= self.MouseSensitivity
        yoffset *= self.MouseSensitivity

        self.Yaw += xoffset
        self.Pitch += -yoffset
        
        # make sure that when pitch is out of bounds, screen doesn't get flipped
        if constrainPitch:
            if self.Pitch > 89.0:
                self.Pitch = 89.0
            if self.Pitch < -89.0:
                self.Pitch = -89.0

        # update Front, Right and Up Vectors using the updated Euler angles
        self.updateCameraVectors()

    # processes input received from a mouse scroll-wheel event. Only requires input on the vertical wheel-axis
    def ProcessMouseScroll(self, yoffset: float) -> None:
        self.Zoom -= yoffset
        if self.Zoom < 1.0:
            self.Zoom = 1.0
        if self.Zoom > 45.0:
            self.Zoom = 45.0

    # calculates the front vector from the Camera's (updated) Euler Angles
    def updateCameraVectors(self) -> None:
        # calculate the new Front vector
        front = glm.vec3()
        front.x = glm.cos(glm.radians(self.Yaw)) * glm.cos(glm.radians(self.Pitch))
        front.y = glm.sin(glm.radians(self.Pitch))
        front.z = glm.sin(glm.radians(self.Yaw)) * glm.cos(glm.radians(self.Pitch))
        self.Front = glm.normalize(front)
        # also re-calculate the Right and Up vector
        self.Right = glm.normalize(
            glm.cross(self.Front, self.WorldUp)
        )  # glm.normalize the vectors, because their length gets closer to 0 the more you look up or down which results in slower movement.
        self.Up = glm.normalize(glm.cross(self.Right, self.Front))

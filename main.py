import glm
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_NEAREST

from Camera2D import Camera2D
from core.display import Window
from core.texture import Texture
from core.utils import loadJSON
from entity import Entity
from level.level import Level
from level.map import Map
from scene import Scene
from sprite import SpriteRenderer

WIDTH = 64 * 16
HEIGHT = 64 * 9
TITLE = "GL_Window"
xOffset = 0.0
step = 0.001


def main():
    # Creating Window
    window = Window(WIDTH, HEIGHT, TITLE)

    scene = Scene(window)

    while window.isNotClosed():
        scene.renderScene()
        window.update()
    scene.cleanup()
    window.close()  # terminating the glfw window


if __name__ == "__main__":
    main()

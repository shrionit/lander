import glm

from Camera2D import Camera2D
from camera import Camera
from core.display import Window
from core.texture import Texture
from scene import Scene
from sprite import SpriteRenderer, Sprite

WIDTH = 64 * 16
HEIGHT = 64 * 9
TITLE = "GL_Window"
xOffset = 0.0
step = 0.001


def main():
    # Creating Window
    window = Window(WIDTH, HEIGHT, TITLE)
    # scene = Scene(window)
    # Creating shaders with basic.frag and basic.vert, no need to specify extension
    # scene.setup()
    camera = Camera2D(position=glm.vec3(0, 0, 5.1))
    spriteRenderer = SpriteRenderer()
    tex = Texture("test.jpg")
    sprites = []
    # for y in range(0, window.HEIGHT, 64):
    #     for x in range(0, window.WIDTH, 64):
    #         sprites.append(Sprite(pos=glm.vec2(x, y), size=glm.vec2(64), tex=tex))
    sprites.append(Sprite(pos=glm.vec3(0, 0, 5), size=glm.vec2(64), tex=tex))
    spriteRenderer.process(sprites)
    while window.isNotClosed():
        # scene.renderScene()
        camera.update(spriteRenderer.shader)
        spriteRenderer.renderSprites()
        window.update()
    # scene.cleanup()
    window.close()  # terminating the glfw window


if __name__ == "__main__":
    main()

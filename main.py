import glm

from Camera2D import Camera2D
from camera import Camera
from core.display import Window
from core.texture import Texture
from entity import Entity
from map import Map
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
    camera = Camera2D(position=glm.vec3(0, 0, -5))
    spriteRenderer = SpriteRenderer()
    tex = Texture("test.jpg")
    tile_map = Map(texture=Texture(assets="maps\\Tiles.png"), tileWidth=8, tileHeight=8)
    sprites = [Entity(position=glm.vec3(1, 1, 5), texture=tex)]
    spriteRenderer.process(sprites)
    while window.isNotClosed():
        camera.update(spriteRenderer.shader)
        camera.update(tile_map.shader)
        tile_map.render()
        spriteRenderer.renderSprites()
        window.update()
    tile_map.cleanup()
    window.close()  # terminating the glfw window


if __name__ == "__main__":
    main()

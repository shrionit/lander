from core.display import Window
from scene import Scene

WIDTH = 1366
HEIGHT = 768
TITLE = "GL_Window"
xOffset = 0.0
step = 0.001


def main():
    # Creating Window
    window = Window(WIDTH, HEIGHT, TITLE)
    scene = Scene(window)
    # Creating shaders with basic.frag and basic.vert, no need to specify extension
    scene.setup()
    while window.isNotClosed():
        scene.render()
        window.update()
    scene.cleanup()
    window.close()  # terminating the glfw window


if __name__ == "__main__":
    main()

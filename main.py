from PIL import Image
from OpenGL.GL import *
from glfw import KEY_LEFT, KEY_RIGHT
from entity import Entity
from gmath import *
import glm
from core.display import Window
from core.shader import Shader
from core.texture import Texture
from core.storage import VAO, VBO, IBO
from core.shapes import RECT
from core.utils import getTime
from core.input import set_on_key
from camera import Camera

WIDTH = 1366
HEIGHT = 768
TITLE = "GL_Window"
xOffset = 0.0
step = 0.001


def moveRight():
    global xOffset
    xOffset += step
    xOffset %= 1.0


def moveLeft():
    global xOffset
    xOffset -= step
    xOffset %= 1.0


def main():
    # Creating Window
    window = Window(WIDTH, HEIGHT, TITLE)
    day = Texture(Image.open("assets/grass-field/Grassy Field Day.png"), isimg=True)
    night = Texture(Image.open("assets/grass-field/Grassy Field Night.png"), isimg=True)
    # Creating shaders with basic.frag and basic.vert, no need to specify extension
    shader = Shader(frag="basic", vert="basic")
    camera = Camera(window, glm.vec3(0.0, 0.0, 5.0), glm.vec3(0.0, 1.0, 0.0), shader=shader)

    set_on_key(KEY_RIGHT, moveRight)
    set_on_key(KEY_LEFT, moveLeft)

    # Creating Vertex Array Buffer
    vao = VAO()
    vao.loadBufferToAttribLocation(0, VBO(RECT.vertices))  # Binding vertices buffer to attrib number 0
    vao.loadBufferToAttribLocation(1, VBO(RECT.vertexColors))  # Binding colors buffer to attrib number 1
    vao.loadBufferToAttribLocation(2, VBO(RECT.texCoords), ddim=2)
    vao.loadIndices(IBO(RECT.indices))  # Binding indeces buffer
    entity = Entity(vao=vao, shader=shader)  # type: ignore
    entity.addInstanceLocation(glm.vec3(1, 0, -1))
    day.bind(GL_TEXTURE0)
    night.bind(GL_TEXTURE1)
    shader.attach()  # using shader
    shader.setUniform1("dayTex", 0, "i")
    shader.setUniform1("nightTex", 1, "i")
    while window.isNotClosed():
        camera.update()
        shader.setUniform1("iTime", getTime(), "f")
        shader.setUniform1("xOffset", xOffset, "f")
        
        entity.bind()
        entity.renderInstance(2)
        entity.unbind()
        
        window.update()

    shader.detach()  # unbinding shader
    window.close()  # terminating the glfw window


if __name__ == "__main__":
    main()

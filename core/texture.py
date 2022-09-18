from OpenGL.GL import *
from PIL import Image
import glm, os


class Texture:

    DEFAULT_PATH = os.getcwd() + "\\textures\\"

    def __init__(self, file, isimg=False):
        self.image = Image.open(Texture.DEFAULT_PATH + file) if not isimg else file
        self.tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.tex)
        # texture wrapping params
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # texture filtering params
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        self.flippedImage = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        self.img_data = self.flippedImage.convert("RGBA").tobytes()
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            self.image.width,
            self.image.height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            self.img_data,
        )
        glBindTexture(GL_TEXTURE_2D, 0)

    def getTexID(self):
        return self.tex

    def updateTexture(self, newimage):
        newimg_data = (
            newimage.transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA").tobytes()
        )
        print(newimg_data)
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            newimage.width,
            newimage.height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            newimg_data,
        )

    def bind(self, texUnit=GL_TEXTURE0):
        glActiveTexture(texUnit)
        glBindTexture(GL_TEXTURE_2D, self.tex)

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)


class Material:
    def __init__(self, name, color, highlighted_color):
        self.name = name
        self.color = color
        self.highlighted_color = highlighted_color


class Metal(Material):
    def __init__(
        self,
        name="_",
        color=glm.vec4(1.0, 1.0, 1.0, 1.0),
        sharpness=1.0,
        highlight_color=glm.vec4(1.0, 1.0, 1.0, 1.0),
        intensity=1.0,
        fresnel=1.0,
        mtype=1,
    ):
        super().__init__(name, color, highlight_color)
        self.sharpness = sharpness
        self.intensity = intensity
        self.fresnel = fresnel
        self.type = mtype


class Glass(Material):
    def __init__(
        self,
        name="_",
        color=glm.vec4(1.0, 1.0, 1.0, 1.0),
        IR=1.0,
        highlight_color=glm.vec4(1.0, 1.0, 1.0, 1.0),
        intensity=1.0,
        fresnel=1.0,
        sharpness=1.0,
        transparency=1.0,
    ):
        super().__init__(name, color, highlight_color)
        self.IR = IR
        self.sharpness = sharpness
        self.intensity = intensity
        self.fresnel = fresnel
        self.transparency = transparency


class Plastic(Material):
    def __init__(
        self,
        name="_",
        color=glm.vec4(1.0, 1.0, 1.0, 1.0),
        highlight_color=glm.vec4(1.0, 1.0, 1.0, 1.0),
        intensity=1.0,
        fresnel=1.0,
        sharpness=1.0,
    ):
        super().__init__(name, color, highlight_color)
        self.sharpness = sharpness
        self.intensity = intensity
        self.fresnel = fresnel

from OpenGL.GL import *
from PIL import Image
from .utils import Dict


class FrameBuffer:
    def __init__(self, width, height, **kwargs):
        self._framebuffer = kwargs.get("framebuffer") or glGenFramebuffers(1)
        self._renderbuffer = kwargs.get("renderbuffer") or glGenRenderbuffers(1)
        self._fb_attachment = kwargs.get("texture") or glGenTextures(1)
        self.window_width, self.window_height = width, height
        self._output = self._compile()

    def getFB(self):
        return self._output

    def _compile(self):
        # binding frame buffer
        glBindFramebuffer(GL_FRAMEBUFFER, self._framebuffer)
        # binding attachment texture
        glBindTexture(GL_TEXTURE_2D, self._fb_attachment)
        # binding render buffer (a direct rendered frame storage without conversion to img format)
        glBindRenderbuffer(GL_RENDERBUFFER, self._renderbuffer)

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGB,
            self.window_width,
            self.window_height,
            0,
            GL_RGB,
            GL_UNSIGNED_BYTE,
            None,
        )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # glTexImage2D(
        #     GL_TEXTURE_2D, 0, GL_DEPTH24_STENCIL8, self.window_width, self.window_height, 0,
        #     GL_DEPTH_STENCIL, GL_UNSIGNED_INT, None
        # )
        glBindTexture(GL_TEXTURE_2D, 0)
        glFramebufferTexture2D(
            GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self._fb_attachment, 0
        )

        glRenderbufferStorage(
            GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, self.window_width, self.window_height
        )

        glBindRenderbuffer(GL_RENDERBUFFER, 0)

        glFramebufferRenderbuffer(
            GL_FRAMEBUFFER,
            GL_DEPTH_STENCIL_ATTACHMENT,
            GL_RENDERBUFFER,
            self._renderbuffer,
        )

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("ERROR: Frame Buffer is Not complete")

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        return Dict(
            {
                "textureId": self._fb_attachment,
                "framebufferId": self._framebuffer,
                "renderbufferId": self._renderbuffer,
            }
        )

    def saveTextureToFile(self, filepath: str, format="PNG"):
        self.attach()
        imgdata = glReadPixels(
            0, 0, self.window_width, self.window_height, GL_RGBA, GL_UNSIGNED_BYTE
        )
        img = Image.frombytes("RGBA", (self.window_width, self.window_height), imgdata)
        img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        filepath += f".{format.lower()}" if filepath.rfind(".") == -1 else ""
        img.save(filepath, format)
        self.detach()

    def attach(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self._framebuffer)

    def detach(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

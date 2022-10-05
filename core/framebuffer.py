from OpenGL.GL import *
from OpenGL.GL.framebufferobjects import glBindFramebuffer
from core.logger import createLogger
from core.display import Window
from core.texture import Texture

logger = createLogger("FBO")

class Framebuffer:
    FBOS = []
    RBOS = []

    def __init__(self, width=Window.WIDTH, height=Window.HEIGHT, multiSample=False, texID=None):
        self.textureID = None
        self.rbo = None
        self.multiSample = multiSample
        self.fbo = None
        self.width = width
        self.height = height
        self.initFBO(texID)

    def initFBO(self, texID=None):
        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        self.textureID = texID or Texture.createCleanTexture(self.width, self.height)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.textureID, 0)
        self.rbo = self.initRBO()
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, self.rbo)
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            logger.error("Frame buffer is not complete!")
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        Framebuffer.FBOS.append(self.fbo)

    def initRBO(self, attachment=GL_DEPTH24_STENCIL8):
        """Creating and returning a render buffer which is similar to a texture buffer
        but the data is in raw bytes and write only and very fast"""
        rbo = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, rbo)
        glRenderbufferStorage(GL_RENDERBUFFER, attachment, self.width, self.height)
        Framebuffer.RBOS.append(rbo)
        return rbo

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glViewport(0, 0, self.width, self.height)

    def unbind(self):
        glViewport(0, 0, Window.WIDTH, Window.HEIGHT)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    @staticmethod
    def cleanUP():
        glDeleteFramebuffers(len(Framebuffer.FBOS), Framebuffer.FBOS)
        glDeleteRenderbuffers(len(Framebuffer.RBOS), Framebuffer.RBOS)

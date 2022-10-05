from abc import abstractmethod
import glm
from OpenGL.GL import glDrawElements, glDrawArrays, GL_TRIANGLES, GL_UNSIGNED_INT

from core.display import Window
from core.shader import Shader
from core.storage import VAO
from core.texture import Texture
from gmath import createTransformationMatrix


class Entity:
    def __init__(
            self,
            position: glm.vec3 = glm.vec3(0),
            rotation: glm.vec3 = glm.vec3(),
            scale: glm.vec3 = glm.vec3(1),
            vao: VAO = None,
            texture: Texture = None,
            shader: Shader = None,
            texOffset: glm.vec2 = glm.vec2(0),
            texMovementMult: float = 1.0
    ) -> None:
        self.texMovementMult = texMovementMult
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.vao: VAO = vao
        self.texture = texture
        self.texOffset = texOffset
        self.shader = shader
        self.instanceLocations = [*self.position.to_list() * 4]

    @abstractmethod
    def getTransformationMatrix(self):
        return createTransformationMatrix(self.position, self.rotation, self.scale)

    @abstractmethod
    def update(self, shader: Shader = None):
        shader = shader or self.shader
        if shader is not None:
            shader.loadTransformationMatrix(self.getTransformationMatrix())

    def getRightTexOffset(self):
        ts = self.texMovementMult * Window.get_deltatime()
        self.texOffset += glm.vec2(ts)
        if self.texOffset.x > 1.0: self.texOffset.x = 0.0
        if self.texOffset.y > 1.0: self.texOffset.y = 0.0
        return self.texOffset

    def getLeftTexOffset(self):
        ts = self.texMovementMult * Window.get_deltatime()
        self.texOffset -= glm.vec2(ts)
        if self.texOffset.x > 1.0: self.texOffset.x = 0.0
        if self.texOffset.y > 1.0: self.texOffset.y = 0.0
        return self.texOffset

    def moveTo(self, newPosition):
        self.position = newPosition

    def setVao(self, vao):
        self.vao = vao

    def bind(self):
        self.vao.bind()

    def unbind(self):
        self.vao.unbind()

    @abstractmethod
    def render(self):
        self.update()
        self.texture.bind()
        if self.vao.hasIndices:
            self.bind()
            glDrawElements(GL_TRIANGLES, self.vao.indicesCount, GL_UNSIGNED_INT, None)
            self.unbind()
        else:
            self.bind()
            glDrawArrays(GL_TRIANGLES, 0, self.vao.vertexCount)
            self.unbind()
        self.texture.unbind()


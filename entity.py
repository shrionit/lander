from turtle import pos
import glm
from OpenGL.GL import glDrawElements, glDrawArrays, glDrawArraysInstanced, glDrawElementsInstanced, GL_TRIANGLES, GL_UNSIGNED_INT
from core.shader import Shader
from core.storage import VAO, VBO
from core.texture import Texture
from gmath import createTransformationMatrix


class Entity:
    def __init__(
        self,
        position: glm.vec3 = glm.vec3(0),
        rotation: glm.vec3 = glm.vec3(),
        scale: glm.vec3 = glm.vec3(1),
        vao: VAO = None,  # type: ignore
        texture: Texture = None,  # type: ignore
        shader: Shader = None  # type: ignore
    ) -> None:
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.vao: VAO = vao
        self.texture = texture
        self.shader = shader
        self.instanceLocations = [*self.position.to_list()*4]

    def GetModelMatrix(self, position=None, rotation=None, scale=None):
        position = position or self.position
        rotation = rotation or self.rotation
        scale = scale or self.scale
        return createTransformationMatrix(position, rotation, scale)
    
    def update(self):
        if self.shader is not None:
            self.shader.loadTransformationMatrix(self.GetModelMatrix())

    def moveTo(self, newPosition):
        self.position = newPosition
        
    def addInstanceLocation(self, newInstanceLocation):
        self.instanceLocations.extend(newInstanceLocation.to_list()*4)
        self.bind()
        self.vao.loadBufferToAttribLocation(3, VBO(self.instanceLocations))
        self.unbind()

    def setVao(self, vao):
        self.vao = vao

    def bind(self):
        self.vao.bind()

    def unbind(self):
        self.vao.unbind()

    def render(self):
        self.update()
        if self.vao.hasIndices:
            self.bind()
            glDrawElements(GL_TRIANGLES, self.vao.indicesCount, GL_UNSIGNED_INT, None)
            self.unbind()
        else:
            self.bind()
            glDrawArrays(GL_TRIANGLES, 0, self.vao.vertexCount)
            self.unbind()
    
    def renderInstance(self, count):
        self.update()
        if self.vao.hasIndices:
            self.bind()
            glDrawElementsInstanced(GL_TRIANGLES, self.vao.indicesCount, GL_UNSIGNED_INT, None, count)
            self.unbind()
        else:
            self.bind()
            glDrawArraysInstanced(GL_TRIANGLES, 0, self.vao.vertexCount, count)
            self.unbind()

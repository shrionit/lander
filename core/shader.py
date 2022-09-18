import os
from abc import ABC
from abc import abstractmethod
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import glm
import numpy as np


class Shader(ABC):

    DEFAULT_PATH = os.getcwd() + "\\shaders\\"

    def __init__(self, frag="fragment", vert="vertex"):
        if frag != "fragment":
            self.modified = True
        else:
            self.modified = False
        self._default_frag = frag
        self._default_vert = vert
        self.shaderVertex = compileShader(
            self.loadShader(self._default_vert, stype="vert"), GL_VERTEX_SHADER
        )
        self.shaderFragment = compileShader(
            self.loadShader(self._default_frag, stype="frag"), GL_FRAGMENT_SHADER
        )
        self.shaderProgram = compileProgram(self.shaderVertex, self.shaderFragment)
        # self.getAllUniformLocations()
        self.uniformLocations = []

    def start(self):
        for l in self.uniformLocations:
            glVertexAttribPointer(l, 3, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(l)
        glUseProgram(self.shaderProgram)

    def attach(self):
        glUseProgram(self.shaderProgram)

    def detach(self):
        glUseProgram(0)

    def stop(self):
        glUseProgram(0)
        glDeleteShader(self.shaderVertex)
        glDeleteShader(self.shaderFragment)

    def loadShader(self, name, stype=""):
        read = open(Shader.DEFAULT_PATH + name + "." + stype, "r")
        out = read.read()
        read.close()
        return out

    def updateShader(self, newshaderfile, stype=GL_FRAGMENT_SHADER):
        glAttachShader(
            self.shaderProgram,
            compileShader(self.loadShader(newshaderfile, "frag"), stype),
        )

    def getAllUniformLocations(self):
        self.location_color = glGetAttribLocation(self.shaderProgram, "setColor")

    def getUniformLocationOfVariable(self, name):
        loc = glGetUniformLocation(self.shaderProgram, name)
        self.uniformLocations.append(loc)
        return loc

    def kindOfDataStoredInPosition(self, position, NumberOfPoints):
        glVertexAttribPointer(position, NumberOfPoints, GL_FLOAT, GL_FALSE, 0, None)

    def setUniform1(self, location, value, dtype="f"):
        loc = glGetUniformLocation(self.shaderProgram, location)
        eval(f"glUniform1{dtype}")(loc, value)

    def setUniformVec3(self, location, value, dtype="f"):
        loc = glGetUniformLocation(self.shaderProgram, location)
        eval(f"glUniform3{dtype}v")(loc, 1, value)

    def putDataInUniformLocation(self, location, data, dtype="f"):
        loc = glGetUniformLocation(self.shaderProgram, location)
        if dtype == "f":
            if type(data) in [np.float32, float]:
                eval(f"glUniform1f")(loc, data)
            else:
                dl = len(data)
                eval(f"glUniform{dl}f")(loc, *data)
        else:
            glUniform1i(loc, data)

    def loadViewMatrix(self, matrix_view):
        self.location_viewMatrix = glGetUniformLocation(
            self.shaderProgram, "viewMatrix"
        )
        glUniformMatrix4fv(self.location_viewMatrix, 1, GL_FALSE, matrix_view.to_list())

    def loadTransformationMatrix(self, matrix_transformation):
        self.location_transformationMatrix = glGetUniformLocation(
            self.shaderProgram, "modelMatrix"
        )
        glUniformMatrix4fv(
            self.location_transformationMatrix,
            1,
            GL_FALSE,
            matrix_transformation.to_list(),
        )

    def loadProjectionMatrix(self, matrix_projection):
        self.location_projectionMatrix = glGetUniformLocation(
            self.shaderProgram, "projectionMatrix"
        )
        glUniformMatrix4fv(
            self.location_projectionMatrix, 1, GL_FALSE, matrix_projection.to_list()
        )

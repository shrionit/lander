import glm
import numpy as np


def createTransformationMatrix(position, rotation, size):
    """Takes -
    translate :glm::vec3
    rotate :glm::vec3
    scale :glm.vec3
    """
    transformation = glm.translate(glm.mat4(1.0), position)
    transformation = glm.rotate(transformation, rotation.x, glm.vec3(1, 0, 0))
    transformation = glm.rotate(transformation, rotation.y, glm.vec3(0, 1, 0))
    transformation = glm.rotate(transformation, rotation.z, glm.vec3(0, 0, 1))
    transformation = glm.scale(transformation, size)
    return transformation


def randomVec3(rmin=-1, rmax=1):
    return glm.vec3(
        np.random.uniform(rmin, rmax),
        np.random.uniform(rmin, rmax),
        np.random.uniform(rmin, rmax)
    )

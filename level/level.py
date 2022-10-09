from OpenGL.raw.GL.VERSION.GL_1_0 import GL_NEAREST

from Camera2D import Camera2D
from core.shader import Shader
from core.texture import Texture
from core.utils import loadJSON, Dict
from .map import Map


class Level:
    def __init__(self, levelFile="level0.tmj", camera: Camera2D = None):
        lvl = loadJSON(f"levels\\{levelFile}")
        [tilemap] = lvl["tilesets"]
        texFile = tilemap["image"].split("/")[-1]
        self.texMap = Texture(assets="maps\\" + texFile, filter=GL_NEAREST)
        self.camera = camera
        lvl = lvl["layers"]
        self.mapshader = Shader(frag="mapShader", vert="mapShader")
        self.layers = Dict()
        for layer in lvl:
            self.layers[layer["id"]] = Dict(
                {
                    "name": layer["name"],
                    "map": Map(
                        self.texMap,
                        level=layer["data"],
                        shader=self.mapshader,
                        tileWidth=tilemap["tilewidth"],
                        tileHeight=tilemap["tileheight"],
                    ),
                }
            )
        print(self.layers)

    def draw(self):
        self.camera.update(self.mapshader)
        for layers in self.layers.values():
            layers.map.render()

    def cleanup(self):
        for layer in self.layers.values():
            layer.map.cleanup()

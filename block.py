from pyglet.gl import *

import pyglet

class Block:
    def __init__(self):
        null = self.load_texture('./assets/minecraft/textures/blocks/null.png')
        block_null = {"oku": null,
             "temae": null,
             "sita": null,
             "ue": null,
             "migi": null,
             "hidari": null
        }
        self.blocks = {"null": block_null}
        self.addNormalBlocks()

    def addNormalBlocks(self):
        self.addNewBlock("dirt", "dirt", "dirt", "dirt", "dirt", "dirt", "dirt")
        self.addNewBlock("test001", "grass_side", "grass_side", "dirt", "dirt", "grass_side", "grass_side")

    def addNewBlock(self, sysId, a, b, c, d, e, f):
        block = {"oku":self.load_texture('./assets/minecraft/textures/blocks/{}.png'.format(a)),
                 "temae":self.load_texture('./assets/minecraft/textures/blocks/{}.png'.format(b)),
                 "sita":self.load_texture('./assets/minecraft/textures/blocks/{}.png'.format(c)),
                 "ue":self.load_texture('./assets/minecraft/textures/blocks/{}.png'.format(d)),
                 "migi":self.load_texture('./assets/minecraft/textures/blocks/{}.png'.format(e)),
                 "hidari":self.load_texture('./assets/minecraft/textures/blocks/{}.png'.format(f))
        }
        self.blocks[sysId] = block

    def getBlock(self, sysId):
        if sysId in self.blocks:
            return self.blocks[sysId]
        else:
            return self.blocks["null"]

    def load_texture(self, path):
        texture = pyglet.image.load(path).get_texture()
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(texture)
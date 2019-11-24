from enum import Enum

class Material(Enum):
    AIR = 0, True
    STONE = 1, False
    GRASS = 2, False
    DIRT = 3, False
    SWORD = 100, True
    PICKAXE = 101, True

    def getId(self):
        return self.value[0]

    def isTransparent(self):
        return self.value[1]

    def getValues(self):
        return self.value
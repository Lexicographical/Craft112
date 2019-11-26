from enum import Enum

# Material represents a specific type of item/block
class Material(Enum):
    # First value is ID
    # Second value represents if texture should support transparency
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

class Tools:
    tools = set(
        [Material.SWORD, Material.PICKAXE]
    )
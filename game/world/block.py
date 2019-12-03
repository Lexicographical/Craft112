from game.serializable import Serializable

# Represents a block in the world at coordinate (x, y) of type `material`
class Block(Serializable):
    def __init__(self, material, x, y):
        self.material = material
        self.x = x
        self.y = y

    def getType(self):
        return self.material

    def getPosition(self):
        return (self.x, self.y)

    def getSerializables(self):
        dct = {
            "x": self.x,
            "y": self.y,
            "material": self.material.getId()
        }
        return dct
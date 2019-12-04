from game.serializable import Serializable
from game.item.material import Material

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
            "material": self.material.getId(),
            "x": self.x,
            "y": self.y
        }
        return dct

    @staticmethod
    def fromJson(json):
        return Block(Material.fromId(json["material"]), json["x"], json["y"])
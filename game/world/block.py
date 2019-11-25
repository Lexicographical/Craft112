# Represents a block in the world at coordinate (x, y) of type `material`
class Block:
    def __init__(self, material, x, y):
        self.material = material
        self.x = x
        self.y = y

    def getType(self):
        return self.material

    def getPosition(self):
        return (self.x, self.y)
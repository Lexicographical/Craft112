# Top-level class for all blocks in the game
class Block:
    def __init__(self, material, x, y):
        self.material = material
        self.x = x
        self.y = y

    def getType(self):
        return self.material

    def getPosition(self):
        return (self.x, self.y)
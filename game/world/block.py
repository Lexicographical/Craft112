from enum import Enum

# Top-level class for all blocks in the game
class Block:
    def __init__(self, blockType, x, y):
        self.blockType = blockType
        self.x = x
        self.y = y

    def getId(self):
        return self.blockType.value

# Enum of block types
class Blocks(Enum):
    AIR = 0
    STONE = 1
    GRASS = 2
    DIRT = 3
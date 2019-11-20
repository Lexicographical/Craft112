import random
from game.world.block import Block
from game.world.material import Material
from utility.constants import Constants

# TODO: handle world gen. start with superflat
# World contains all the entities and blocks loaded in the game
class World:
    def __init__(self):
        self.seed = random.randrange(1, (1 << 32) - 1)
        self.width = Constants.WORLD_WIDTH
        self.height = Constants.WORLD_HEIGHT
        
        self.wOffset = Constants.WORLD_WIDTH // 2
        self.hOffset = Constants.WORLD_HEIGHT // 2

        self.blocks = []
        self.entities = set()

    def generateWorld(self):
        for j in range(self.height):
            self.blocks.append([])
            for i in range(self.width):
                x, y = self.indexToCoordinate((i, j))
                blockType = Material.DIRT
                if y > 0:
                    blockType = Material.AIR
                self.blocks[j].append(Block(blockType, x, y))
        print("World Size:", len(self.blocks), len(self.blocks[0]))

    def indexToCoordinate(self, index):
        i, j = index
        return (i - self.wOffset, j - self.hOffset)
    
    def coordinateToIndex(self, coordinate):
        x, y = coordinate
        return (x + self.wOffset, y + self.hOffset)
    
    def setBlock(self, blockType, coordinate):
        i, j = [int(k) for k in self.coordinateToIndex(coordinate)]
        self.blocks[j][i] = Block(blockType, i, j)

    def getBlock(self, coordinate):
        i, j = [int(k) for k in self.coordinateToIndex(coordinate)]
        if i < 0 or i >= self.width or j < 0 or j >= self.height:
            return Constants.AIR_BLOCK
        block = self.blocks[j][i]
        return block
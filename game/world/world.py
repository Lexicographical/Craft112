import random
from noise import snoise2
from game.world.block import Block
from game.item.material import Material
from utility.constants import Constants
from utility.utility import Utility
from game.entity.enemy import Enemy
from game.entity.entity import *

# TODO: blit all tiles for 100 radius then re-render as necessary
class World:
    def __init__(self):
        self.seed = random.randrange(1, Constants.SEED_MAX)
        self.width = Constants.WORLD_WIDTH
        self.height = Constants.WORLD_HEIGHT
        
        self.wOffset = Constants.WORLD_WIDTH // 2
        self.hOffset = Constants.WORLD_HEIGHT // 2
        
        print("Offsets", self.wOffset, self.hOffset)

        self.blocks = []
        self.entities = set()

    def generateElevations(self):
        elevation = [0] * self.width
        base = self.height / 4
        j = self.seed / Constants.SEED_MAX
        for i in range(self.width):
            elevation[i] += snoise2(i/self.width, j, 4)
            elevation[i] += snoise2(i/self.width, j, 16)
            elevation[i] *= base
        return elevation

    def generateWorld(self):
        elevation = self.generateElevations()
        # elevation = [0]*self.width
        # for i in range(self.width):
        #     if i & 3:
        #         elevation[i] = -1
        #     else:
        #         elevation[i] = 1
        for j in range(self.height):
            self.blocks.append([])
            for i in range(self.width):
                self.blocks[j].append(None)
        for i in range(self.width):
            for j in range(self.height):
                x, y = self.indexToCoordinate((i, j))
                blockType = Material.DIRT
                if y == int(elevation[i]):
                    blockType = Material.GRASS
                elif y > elevation[i]:
                    blockType = Material.AIR
                self.blocks[j][i] = Block(blockType, x, y)

        print("World Size:", len(self.blocks), len(self.blocks[0]))

    def indexToCoordinate(self, index):
        i, j = index
        return (i - self.wOffset, j - self.hOffset)
    
    def coordinateToIndex(self, coordinate):
        x, y = [int(i) for i in coordinate]
        return (x + self.wOffset, y + self.hOffset)
    
    def setBlock(self, blockType, coordinate):
        i, j = [int(k) for k in self.coordinateToIndex(coordinate)]
        self.blocks[j][i] = Block(blockType, i, j)

    def getBlock(self, coordinate, coord=False):
        i, j = [Utility.round(k) for k in coordinate]
        i, j = self.coordinateToIndex((i, j))
        if i < 0 or i >= self.width or j < 0 or j >= self.height:
            if coord:
                return Constants.AIR_BLOCK, (i, j)
            return Constants.AIR_BLOCK
        block = self.blocks[j][i]
        if coord:
            return block, (i, j)
        return block

    def getHighestBlock(self, x):
        x, _ = self.coordinateToIndex((x, 0))
        for j in range(self.height-1, -1, -1):
            if self.blocks[j][x].getType() != Material.AIR:
                _, y = self.indexToCoordinate((0, j))
                return y+1
        print("Max reached")
        _, y = self.indexToCoordinate((0, self.height))
        return y

# TODO: add entity spawning
    def rngSpawnEntity(self, player, spawn=False):
        chance = random.random()
        if spawn or (len(self.entities) <= 3 and chance < 0.1):
            x, _ = player.position
            chance = random.random()
            sign = -1 if chance < 0.5 else 1
            chance = (chance + 0.5) if chance < 0.5 else chance
            offset = chance * 5
            x += sign * (3 + offset)
            y = self.getHighestBlock(x)
            self.spawnEntity((x, y))
            
    def spawnEntity(self, position):
        enemy = Enemy(Entities.ENEMY, self, 20,
                        "enemy", "enemyLeft", "enemyRight", 1)
        enemy.setPosition(position)
        self.entities.add(enemy)
        print("Spawned enemy", position)
import random
import copy
from noise import snoise2
from game.world.block import Block
from game.item.material import Material
from game.world.vector2d import Vector2D
from utility.constants import Constants
from game.entity.enemy import Enemy
from game.entity.entity import *
from game.entity.player import Player
from game.serializable import Serializable
import sys

if "utility.utility" not in sys.modules:
    from utility.utility import Utility

# World stores all the in-game information about the current world
class World(Serializable):
    def __init__(self, name="World 1", seed=None):
        self.name = name
        if seed is None:
            self.seed = random.randrange(1, Constants.SEED_MAX)
        else:
            self.seed = seed
        self.width = Constants.WORLD_WIDTH
        self.height = Constants.WORLD_HEIGHT
        
        self.wOffset = Constants.WORLD_WIDTH // 2
        self.hOffset = Constants.WORLD_HEIGHT // 2
        
        self.blocks = []
        self.entities = set()
        self.player = None

        self.clockTick = 0
        self.spawnTickRate = 10
        self.spawnChances = [0, 0.01, 0.05, 0.1]
        self.difficulty = 2

        self.initBlockMatrix()

    def initBlockMatrix(self):
        for j in range(self.height):
            self.blocks.append([])
            for i in range(self.width):
                self.blocks[j].append(None)

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
        for i in range(self.width):
            for j in range(self.height):
                x, y = self.indexToCoordinate((i, j))
                blockType = Material.STONE
                if y == int(elevation[i]):
                    blockType = Material.GRASS
                elif y > elevation[i]:
                    blockType = Material.AIR
                elif y > elevation[i] - 5:
                    blockType = Material.DIRT
                self.blocks[j][i] = Block(blockType, x, y)

    def indexToCoordinate(self, index):
        i, j = index
        return (i - self.wOffset, j - self.hOffset)
    
    def coordinateToIndex(self, coordinate):
        x, y = [int(i) for i in coordinate]
        return (x + self.wOffset, y + self.hOffset)
    
    def setBlock(self, blockType, coordinate):
        i, j = [Utility.round(k) for k in coordinate]
        i, j = self.coordinateToIndex((i, j))
        self.blocks[j][i] = Block(blockType, i, j)

    def getBlock(self, coordinate):
        i, j = [Utility.round(k) for k in coordinate]
        i, j = self.coordinateToIndex((i, j))
        if i < 0 or i >= self.width or j < 0 or j >= self.height:
            return Constants.AIR_BLOCK
        block = self.blocks[j][i]
        return block

    def getHighestBlock(self, x):
        x, _ = self.coordinateToIndex((x, 0))
        for j in range(self.height-1, -1, -1):
            if self.blocks[j][x].getType() != Material.AIR:
                _, y = self.indexToCoordinate((0, j))
                return y+1
        _, y = self.indexToCoordinate((0, self.height))
        return y

    def rngSpawnEntity(self, player, spawn=False):
        chance = random.random()
        if spawn or (len(self.entities) <= 3 and chance < self.spawnChances[self.difficulty]):
            x, _ = player.position
            chance = random.random()
            sign = 1 if chance > 0.5 else -1
            chance = (chance + 0.5) if chance < 0.5 else chance
            offset = chance * 5
            x += sign * (3 + offset)
            y = self.getHighestBlock(x)
            self.spawnEntity(Vector2D(x, y))
            
    def spawnEntity(self, position):
        if self.difficulty == 0: return
        enemy = Enemy(Entities.ENEMY, self, 1)
        enemy.setPosition(position)
        self.addEntity(enemy)

    def addEntity(self, entity):
        self.entities.add(entity)
        if isinstance(entity, Player):
            self.player = entity

    def removeEntity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def tick(self):
        self.clockTick += 1
        if self.clockTick % self.spawnTickRate == 0:
            self.rngSpawnEntity(self.player)
        cpy = copy.copy(self.entities)
        for entity in cpy:
            entity.update()
            if isinstance(entity, Enemy):
                entity.ai()

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty
        if difficulty == 0:
            ls = []
            for entity in self.entities:
                if not isinstance(entity, Player):
                    ls.append(entity)
            for entity in ls:
                self.entities.remove(entity)
    
    def getSerializables(self):

        dct = {
            "name": self.name,
            "seed": self.seed,
            "width": self.width,
            "height": self.height,
            "difficulty": self.difficulty,
            "blocks": [[block.getSerializables() for block in row] for row in self.blocks]
        }
        entities = {}
        for entity in self.entities:
            entities.update(entity.getSerializables())
        dct["entities"] = entities
        return dct

    @staticmethod
    def fromJson(json):
        world = World(name=json["name"], seed=json["seed"])
        world.width = json["width"]
        world.height = json["height"]
        world.difficulty = json["difficulty"]
        for uuid in json["entities"]:
            string = json["entities"][uuid]
            entity = Entity.fromJson(string, uuid, world)
            world.addEntity(entity)
        for i in range(world.height):
            for j in range(world.width):
                blockJson = json["blocks"][i][j]
                block = Block.fromJson(blockJson)
                world.blocks[i][j] = block
        return world
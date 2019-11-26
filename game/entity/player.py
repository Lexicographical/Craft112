import pygame
from game.entity.entity import *
from utility.assets import Assets
from game.item.material import Material
from game.item.item import ItemStack
from game.entity.inventory import Inventory
from utility.constants import Constants
from game.world.position import Position

# Players are controllable entities 
class Player(Entity):
    def __init__(self, world):
        super().__init__(Entities.PLAYER, world, 20, "player", "playerLeft", "playerRight")
        self.inventory = Inventory(Constants.INVENTORY_WIDTH, Constants.INVENTORY_HEIGHT)
        self.equipIndex = 0
    
    def getInventory(self):
        return self.inventory

    def getEquippedItem(self):
        return self.inventory[0][self.equipIndex]

    def respawn(self):
        self.health = self.maxHealth
        self.isAlive = True

        y = self.world.getHighestBlock(0)
        self.position = Position(0, y)
        self.world.entities.clear()
        self.world.entities.add(self)
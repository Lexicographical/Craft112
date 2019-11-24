import pygame
from game.entity.entity import *
from utility.assets import Assets
from game.item.material import Material
from game.item.item import ItemStack
from game.entity.inventory import Inventory
from utility.constants import Constants

# Player entity
class Player(Entity):
    def __init__(self, world):
        super().__init__(Entities.PLAYER, world, 20, "player", "playerLeft", "playerRight")
        self.inventory = Inventory(Constants.INVENTORY_WIDTH, Constants.INVENTORY_HEIGHT)
        self.equipIndex = 0
    
    def getInventory(self):
        return self.inventory

    def getEquippedItem(self):
        return self.inventory[0][self.equipIndex]
import pygame
from game.entity.entity import *
from utility.assets import Assets
from game.world.material import Material
from game.world.item import ItemStack
from game.entity.inventory import Inventory
from utility.constants import Constants

# Player entity
class Player(Entity):
    def __init__(self):
        super().__init__(Entities.PLAYER, 20, "sprite", "spriteLeft", "spriteRight")
        self.inventory = Inventory(Constants.INVENTORY_WIDTH, Constants.INVENTORY_HEIGHT)
    
    def addItem(self, item):
        return self.inventory.addItem(item)

    

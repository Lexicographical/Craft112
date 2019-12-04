import pygame
from game.entity.entity import *
from utility.assets import Assets
from game.item.material import *
from game.item.item import ItemStack
from game.entity.inventory import Inventory
from utility.constants import Constants
from utility.vector2d import Vector2D

# Players are controllable entities 
class Player(Entity):
    def __init__(self, world):
        super().__init__(Entities.PLAYER, world)
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
        self.position = Vector2D(0, y)
        self.world.entities.clear()
        self.world.entities.add(self)

    def draw(self, window, x, y):
        item = self.getEquippedItem()
        material = item.getType()
        id = material.getId()
        if material in Tools.tools or material in Weapons.weapons:
            texture, alt = Assets.assets["textures"][id]
        else:
            texture = alt = Assets.assets["textures"][id][1]

        width, height = texture.get_size()
        pHeight = self.sprite.get_size()[1]
        offset = [
            [-8, -6, -7, -7, -10, -12, -9, -8, -7],
            [0, 8, 5, -1, -2, -3, -2, -1, 0]
        ]
        vOffset = pHeight/4 + 7

        if self.isLeft[0] or self.isRight[0]:
            rect = pygame.Rect(0, 0, width, height)
            rect.center = (x + offset[self.isRight[0]][self.spriteIndex], y + vOffset)
            if self.isLeft[0]:
                window.blit(alt, rect)
                super().draw(window, x, y)
            elif self.isRight[0]:
                super().draw(window, x, y)
                window.blit(texture, rect)
        else:
            super().draw(window, x, y)

    def getSerializables(self):
        dct = super().getSerializables()
        inv = {
            "width": self.inventory.width,
            "height": self.inventory.height,
            "contents": [[item.getSerializables() for item in row]
                          for row in self.inventory]
        }
        dct[self.uuid]["inventory"] = inv
        return dct

    @staticmethod
    def fromJson(json, world):
        player = Player(world)
        invJson = json["inventory"]
        width, height = invJson["width"], invJson["height"]
        inventory = Inventory(width, height)
        for i in range(height):
            for j in range(width):
                inventory[i][j] = ItemStack.fromJson(invJson["contents"][i][j])
        player.inventory = inventory
        return player
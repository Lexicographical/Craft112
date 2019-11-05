import pygame
from game.entity.entity import *
from utility.assets import Assets

class Player(Entity):
    def __init__(self):
        super().__init__(Entities.PLAYER)
        self.position = [0, 0]

        self.image = Assets.assets["sprite"]
        self.rect = self.image.get_rect()

    def movePlayer(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy
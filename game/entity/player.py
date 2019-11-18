import pygame
from game.entity.entity import *
from utility.assets import Assets
from utility.constants import Constants

# Player entity
class Player(Entity):
    def __init__(self):
        super().__init__(Entities.PLAYER)
        self.position = [0, 0]

        self.image = Assets.assets["sprite"]
        self.rect = self.image.get_rect()

        self.left = False
        self.right = False
        self.isJumping = False

        self.jumpTick = 10
        self.walkTick = 0

    def faceDirection(self, dx, dy):
        if (dx, dy) == (-1, 0):
            self.left = True
            self.right = False
        elif (dx, dy) == (1, 0):
            self.left = False
            self.right = True
        elif (dx, dy) == (0, 0):
            self.left = False
            self.right = False

    def move(self, dx, dy, walk=False):
        self.position[0] += round(dx*0.25, 2)
        self.position[1] += round(dy*0.25, 2)

        if walk:
            self.faceDirection(dx, dy)

    def jump(self):
        self.faceDirection(0, 0)
        self.isJumping = True
        self.walkTick = 0

    def update(self):
        if self.isJumping:
            if self.jumpTick >= -10:
                sign = -1 if self.jumpTick < 0 else 1
                dy = abs(self.jumpTick) * Constants.JUMP_FACTOR * sign
                self.move(0, dy)
                self.jumpTick -= 1
            else:
                self.isJumping = False
                self.jumpTick = 10

    def getPosition(self):
        return "(%.2f, %.2f)" % (self.position[0], self.position[1])

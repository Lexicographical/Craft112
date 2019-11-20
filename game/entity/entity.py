import pygame
from enum import Enum
from utility.constants import Constants
from utility.assets import Assets
import uuid

# Top level class for game entities
class Entity(pygame.sprite.Sprite):
    def __init__(self, type, health, sprite, spriteLeft, spriteRight):
        super().__init__()
        self.type = type
        self.position = [0, 0]
        self.health = health

        self.sprite = Assets.assets[sprite]
        self.spriteLeft = Assets.assets[spriteLeft]
        self.spriteRight = Assets.assets[spriteRight]

        self.rect = self.sprite.get_rect()
        self.isLeft = False
        self.isRight = False
        self.isJumping = False

        self.jumpTick = 10
        self.walkTick = 0

        self.uuid = uuid.uuid4()

    def damage(self, dmg):
        self.health -= dmg

    def faceDirection(self, dx, dy):
        if (dx, dy) == (-1, 0):
            self.isLeft = True
            self.isRight = False
        elif (dx, dy) == (1, 0):
            self.isLeft = False
            self.isRight = True
        elif (dx, dy) == (0, 0):
            self.isLeft = False
            self.isRight = False

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

    def draw(self, window, x, y):
        # create rect for sprite location
        width, height = self.sprite.get_size()
        spriteRect = pygame.Rect(0, 0, width, height)
        spriteRect.center = (x, y)

        # animate sprite walk every other WALK_FACTOR ticks
        spriteIndex = self.walkTick // Constants.WALK_FACTOR
        if self.isLeft:
            window.blit(self.spriteLeft[spriteIndex], spriteRect)
        elif self.isRight:
            window.blit(self.spriteRight[spriteIndex], spriteRect)
        else:
            window.blit(self.sprite, spriteRect)
        self.walkTick += 1

        spriteCount = Constants.SPRITE_COUNT
        if self.walkTick >= spriteCount * Constants.WALK_FACTOR:
            self.walkTick = 0

    def __hash__(self):
        return hash(self.uuid)

# List of all entity types
class Entities(Enum):
    PLAYER = "player"
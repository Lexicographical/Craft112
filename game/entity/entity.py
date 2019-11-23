import pygame
from enum import Enum
from game.world.material import Material
from utility.constants import Constants
from utility.assets import Assets
import uuid
import math

# Top level class for game entities
class Entity(pygame.sprite.Sprite):
    def __init__(self, type, world, health, sprite, spriteLeft, spriteRight):
        super().__init__()
        self.type = type
        self.position = [0, 0]
        self.health = health
        self.world = world

        self.sprite = Assets.assets[sprite]
        self.spriteLeft = Assets.assets[spriteLeft]
        self.spriteRight = Assets.assets[spriteRight]

        self.rect = self.sprite.get_rect()
        self.isLeft = False
        self.isRight = False
        self.isJumping = False

        self.velocY = 0

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

    # TODO: make movement in terms of velocity
    # cancel velocity if collision occurs
    def move(self, dx, dy, walk=False):
        xFactor = round(dx*0.25, 2)

        self.position[0] += xFactor
        self.position[1] += round(dy*0.25, 2)

        world = self.world
        if not (-world.wOffset <= self.position[0] <= world.wOffset):
            self.position[0] -= xFactor

        if walk:
            self.faceDirection(dx, dy)

    def jump(self):
        self.velocY += Constants.GRAVITY*2
        self.isJumping = True
        print("Jump")

    def update(self):
        self.fall()
        world = self.world
        if self.velocY != 0:
            self.isJumping = True
            sign = -1 if self.velocY < 0 else 1
            if self.velocY < 1:
                self.drop(sign)
            else:
                for _ in range(int(abs(self.velocY))):
                    if self.drop(sign):
                        break
        else:
            x, y = self.position
            block = world.getBlock((x, y))
            if block.getType() != Material.AIR:
                self.position[1] += 1
            
        # if self.isJumping:
        #     if self.jumpTick >= -10:
        #         sign = -1 if self.jumpTick < 0 else 1
        #         dy = abs(self.jumpTick) * Constants.JUMP_FACTOR * sign
        #         self.move(0, dy)
        #         self.jumpTick -= 1
        #     else:
        #         self.isJumping = False
        #         self.jumpTick = 10

    def drop(self, sign):
        world = self.world
        self.position[1] += sign
        x, y = self.position
        block = world.getBlock((x, y))
        if block.getType() != Material.AIR:
            self.velocY = 0
            self.position[1] -= sign
            self.isJumping = False
    
    def fall(self):
        x, y = self.position
        world = self.world
        block = world.getBlock((x, y-1))
        if block.getType() == Material.AIR:
            self.velocY -= Constants.GRAVITY
            return True
        return False

    def getPosition(self):
        return "(%.2f, %.2f)" % (self.position[0], self.position[1])

    def draw(self, window, x, y):
        # create rect for sprite location
        width, height = self.sprite.get_size()
        spriteRect = pygame.Rect(0, 0, width, height)
        spriteRect.center = (x, y+height/4)

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
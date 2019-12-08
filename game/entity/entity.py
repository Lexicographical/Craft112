import math
import uuid
from enum import Enum
from threading import Timer
import pygame
from game.item.material import Material
from game.serializable import Serializable
from utility.vector2d import Vector2D
from utility.assets import Assets
from utility.colors import Colors
from utility.constants import Constants


# Top level class for game entities
class Entity(pygame.sprite.Sprite, Serializable):
    def __init__(self, type, world):
        super().__init__()
        self.type = type
        self.world = world

        self.position = Vector2D(0, 0)
        self.velocity = Vector2D(0, 0)

        self.maxHealth = self.type.getMaxHealth()
        self.health = self.maxHealth

        self.isAlive = True
        self.isBurning = False
        self.isFrozen = False

        self.statusTick = 0

        sprite, spriteLeft, spriteRight = type.getSpriteLabels()

        self.sprite = Assets.assets[sprite]
        self.spriteLeft = Assets.assets[spriteLeft]
        self.spriteRight = Assets.assets[spriteRight]

        self.rect = self.sprite.get_rect()
        self.isLeft = False, False
        self.isRight = False, False
        self.isJumping = False

        self.walkTick = 0
        self.spriteIndex = 0

        self.uuid = str(uuid.uuid4())

    def damage(self, dmg, dx, knockback=True):
        self.health -= dmg
        if knockback:
            self.doKnockback(dx)
        if self.health <= 0:
            self.health = 0
            self.isAlive = False
            self.world.removeEntity(self)

    def doKnockback(self, dx):
        if self.velocity[0] == 0:
            self.velocity[0] += dx*Constants.GRAVITY
        if self.velocity[1] == 0:
            self.velocity[1] += Constants.GRAVITY

    def burn(self):
        self.isFrozen = False
        self.isBurning = True
        self.statusTick = 5
        self.updateStatus()

    def freeze(self):
        self.isBurning = False
        self.isFrozen = True
        self.statusTick = 5
        self.updateStatus()

    def updateStatus(self):
        self.statusTick -= 1
        if self.isBurning:
            self.damage(Constants.BURN_DAMAGE, 0, knockback=True)
        if self.statusTick > 0:
            Timer(1, self.updateStatus, ()).start()
        else:
            self.isBurning = False
            self.isFrozen = False

    def faceDirection(self, dx, moving):
        if dx < 0:
            self.isLeft = True, moving
            self.isRight = False, False
        elif dx > 0:
            self.isLeft = False, False
            self.isRight = True, moving
        elif dx == 0:
            self.isLeft = False, False
            self.isRight = False, False

    def move(self, dx, dy, walk=False):
        if self.isFrozen: return True
        xFactor = round(dx*0.2, 2)

        self.position[0] += xFactor
        self.position[1] += round(dy*0.25, 2)

        world = self.world
        block = self.world.getBlock(self.position)
        if (not (-world.wOffset <= self.position[0] <= world.wOffset) or
            block.getType() != Material.AIR):
            self.position[0] -= xFactor
            return False
        if walk:
            self.faceDirection(dx, True)
        return True

    def jump(self):
        if self.isJumping: return
        self.velocity[1] += Constants.GRAVITY*2
        self.isJumping = True

    # make the entity fall and/or update position based on current position and velocity
    def update(self):
        self.fall()
        self.updatePosition()

    # update position of the entity based on the current velocity
    def updatePosition(self):
        world = self.world
        for axis in range(len(self.velocity)):
            velocity = self.velocity[axis]
            if velocity != 0:
                if axis == 1:
                    self.isJumping = True
                sign = 1 if velocity > 0 else -1

                if abs(velocity) < 1:
                    self.shift(axis, sign)
                else:
                    velocity = int(abs(velocity))
                    for _ in range(velocity):
                        if self.shift(axis, sign):
                            break

                if axis == 0:
                    self.velocity[axis] -= sign*Constants.AIR_RESISTANCE
                    if self.velocity[axis]*sign < 0:
                        self.velocity[axis] = 0
            else:
                x, y = self.position
                block = world.getBlock((x, y))
                if block.getType() != Material.AIR:
                    self.position[axis] += 1

    # shift the position of entity by sign in the direction of the axis
    def shift(self, axis, sign):
        self.position[axis] += sign
        x, y = self.position
        world = self.world
        block = world.getBlock((x, y))
        if block.getType() != Material.AIR:
            self.velocity[axis] = 0
            self.position[axis] -= sign
            if axis == 1:
                self.isJumping = False
    
    # drop the entity if the block below is air (simulate gravity)
    def fall(self):
        x, y = self.position
        world = self.world
        block = world.getBlock((x, y-1))
        if block.getType() == Material.AIR:
            self.velocity[1] -= Constants.GRAVITY
            return True
        return False

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    def draw(self, window, x, y):
        self.drawSprite(window, x, y)
        self.drawHealthBar(window, x, y)

    def drawSprite(self, window, x, y):
        # create rect for sprite location
        width, height = self.sprite.get_size()
        spriteRect = pygame.Rect(0, 0, width, height)
        spriteRect.center = (x, y+height/4)

        # animate sprite walk every other WALK_FACTOR ticks
        self.spriteIndex = self.walkTick // Constants.WALK_FACTOR
        if self.isLeft[0]:
            window.blit(self.spriteLeft[self.spriteIndex], spriteRect)
            if not self.isFrozen:
                self.walkTick += self.isLeft[1]
        elif self.isRight[0]:
            window.blit(self.spriteRight[self.spriteIndex], spriteRect)
            if not self.isFrozen:
                self.walkTick += self.isRight[1]
        else:
            window.blit(self.sprite, spriteRect)

        if self.walkTick >= len(self.spriteLeft) * Constants.WALK_FACTOR:
            self.walkTick = 0

    def drawHealthBar(self, window, x, y):
        healthBarWidth = 50
        healthBarHeight = 10

        rect = pygame.Rect(0, 0, healthBarWidth, healthBarHeight)
        rect.center = (x, y-healthBarHeight*2)

        greenWidth = (self.health / self.maxHealth) * healthBarWidth
        greenRect = pygame.Rect(0, 0, greenWidth, healthBarHeight)
        greenRect.topleft = rect.topleft
        
        pygame.draw.rect(window, Colors.RED, rect)
        pygame.draw.rect(window, Colors.GREEN, greenRect)
        pygame.draw.rect(window, Colors.BLACK, rect, 1)

    def __hash__(self):
        return hash(self.uuid)

    def getSerializables(self):
        dct = {
            self.uuid: {
                "type": self.type.getType(),
                "health": self.health,
                "position": str(self.position),
                "velocity": str(self.velocity)
            }
        }
        return dct
    
    @staticmethod
    def fromJson(json, uuid, world):
        entity = None
        if json["type"] == "player":
            from game.entity.player import Player
            entity = Player.fromJson(json, world)
        elif json["type"] == "enemy":
            from game.entity.enemy import Enemy
            entity = Enemy.fromJson(json, world)
        else:
            raise Exception("[Entity::fromJson] Unknown entity type encountered!")
            
        if entity is not None:
            entity.uuid = uuid
            entity.health = json["health"]
            entity.position = Vector2D.parse(json["position"])
            entity.velocity = Vector2D.parse(json["velocity"])
        
        return entity

# List of all entity types
class Entities(Enum):
    PLAYER = "player", 20, "player", "playerLeft", "playerRight"
    ENEMY = "enemy", 20, "enemy", "enemyLeft", "enemyRight"

    def getType(self):
        return self.value[0]
    
    def getMaxHealth(self):
        return self.value[1]

    def getSpriteLabels(self):
        return self.value[2:5]

    @staticmethod
    def fromType(type):
        for entity in Entities:
            if entity.getType() == type:
                return entity

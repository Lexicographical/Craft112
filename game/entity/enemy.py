from game.entity.entity import *

class Enemy(Entity):
    def __init__(self, enemyType, world, health, sprite, spriteLeft, spriteRight):
        super().__init___(enemyType, world, health, sprite, spriteLeft, spriteRight)
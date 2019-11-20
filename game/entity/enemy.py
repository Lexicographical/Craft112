from game.entity.entity import *

class Enemy(Entity):
    def __init__(self, enemyType, health, sprite, spriteLeft, spriteRight):
        super().__init___(enemyType, health, sprite, spriteLeft, spriteRight)
from game.entity.entity import *

class Enemy(Entity):
    def __init__(self, entityType, world, health,
                 sprite, spriteLeft, spriteRight, damage):
        super().__init__(entityType, world, health,
                          sprite, spriteLeft, spriteRight)

        self.base_damage = damage
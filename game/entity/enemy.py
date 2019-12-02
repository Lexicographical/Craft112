from game.entity.entity import *
import math

# Enemies are entities that will follow and attack the player
class Enemy(Entity):
    def __init__(self, entityType, world, health,
                 sprite, spriteLeft, spriteRight, damage):
        super().__init__(entityType, world, health,
                          sprite, spriteLeft, spriteRight)

        self.base_damage = damage
        self.base_speed = 0.25
        self.followThreshold = 20

    def ai(self, player):
        ePos = self.position
        pPos = player.position
        if ePos.distance(pPos) <= self.followThreshold:
            ex = ePos[0]
            px = pPos[0]
            dx = self.base_speed if px > ex else -self.base_speed
            collide = not self.move(dx, 0, walk=True)
            if collide:
                self.jump()
            if abs(ex-px) < 1:
                player.damage(self.base_damage, dx)
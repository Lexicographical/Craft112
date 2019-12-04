from game.entity.entity import *
import math
from game.entity.player import Player

# Enemies are entities that will follow and attack the player
class Enemy(Entity, Serializable):
    def __init__(self, entityType, world, damage):
        super().__init__(entityType, world)

        self.base_damage = damage
        self.base_speed = 0.25
        self.followThreshold = 20

    def ai(self):
        player = None
        bestDistance = float("inf")
        ePos = self.position
        for entity in self.world.entities:
            if isinstance(entity, Player):
                dist = ePos.distance(entity.position)
                if dist < bestDistance:
                    bestDistance = dist
                    player = entity
                    
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

    def getSerializables(self):
        dct = super().getSerializables()
        dct[self.uuid]["base_damage"] = self.base_damage
        return dct

    @staticmethod
    def fromJson(json, world):
        enemy = Enemy(Entities.ENEMY, world, json["base_damage"])
        return enemy
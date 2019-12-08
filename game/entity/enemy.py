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

    # Perform the AI for enemies if they are not frozen
    # Looks for the closest player and follows it
    # if it encounters a block, jump over it
    def ai(self):
        if self.isFrozen: return
        player = None
        bestDistance = float("inf")
        ePos = self.position
        for entity in self.world.entities:
            if isinstance(entity, Player):
                dist = ePos.distance(entity.position)
                if dist < bestDistance:
                    bestDistance = dist
                    player = entity
        if player is None:
            return            
        ePos = self.position
        pPos = player.position
        if ePos.distance(pPos) <= self.followThreshold:
            ex = ePos[0]
            px = pPos[0]
            dx = self.base_speed if px > ex else -self.base_speed
            collide = not self.move(dx, 0, walk=True)
            if collide:
                self.jump()
            if ePos.distance(pPos) <= 1:
                player.damage(self.base_damage, dx)

    def getSerializables(self):
        dct = super().getSerializables()
        dct[self.uuid]["base_damage"] = self.base_damage
        return dct

    @staticmethod
    def fromJson(json, world):
        enemy = Enemy(Entities.ENEMY, world, json["base_damage"])
        return enemy
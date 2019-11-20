from enum import Enum
from game.world.material import Material
import uuid

class ItemStack:
    def __init__(self, material, amount):
        self.material = material
        self.amount = amount
        self.uuid = uuid.uuid4()

    def getMaterial(self):
        return self.material

    def getAmount(self):
        return self.amount

    def __hash__(self):
        return hash(self.uuid)
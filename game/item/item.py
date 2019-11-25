from enum import Enum
from game.item.material import Material
import uuid

class ItemStack:
    def __init__(self, material, amount):
        self.material = material
        self.amount = amount
        self.uuid = uuid.uuid4()

    def getType(self):
        return self.material

    def getAmount(self):
        return self.amount

    def __hash__(self):
        return hash(self.uuid)
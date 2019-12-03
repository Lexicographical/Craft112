from enum import Enum
from game.item.material import Material
import uuid
from game.serializable import Serializable

# An itemstack represents a stack of `amount` items of type `material`
class ItemStack(Serializable):
    def __init__(self, material, amount):
        self.material = material
        self.amount = amount

    def getType(self):
        return self.material

    def getAmount(self):
        return self.amount

    def setAmount(self, amount):
        self.amount = amount

    def getSerializable(self):
        return {
            "material": self.material,
            "amount": self.amount,
        }
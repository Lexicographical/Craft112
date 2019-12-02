from enum import Enum

# Material represents a specific type of item/block
class Material(Enum):
    # First value is ID
    # Second value represents if texture should support transparency
    AIR = 0, True
    STONE = 1, False
    GRASS = 2, False
    DIRT = 3, False
    SWORD = 100, True
    PICKAXE = 101, True

    def getId(self):
        return self.value[0]

    def isTransparent(self):
        return self.value[1]

    def getValues(self):
        return self.value

    def __hash__(self):
        return hash(self.getValues())

class MeleeWeapon:
    def __init__(self, material, damage, reach):
        self.material = material
        self.damage = damage
        self.reach = reach

class Tools:
    tools = {
        Material.SWORD: MeleeWeapon(Material.SWORD, 5, 2),
        Material.PICKAXE: None
    }
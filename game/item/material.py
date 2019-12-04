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
    FIRE_SWORD = 101, True
    ICE_SWORD = 102, True
    PICKAXE = 200, True
    EXPLOSIVE_PICKAXE = 201, True

    def getId(self):
        return self.value[0]

    def isTransparent(self):
        return self.value[1]

    def getValues(self):
        return self.value

    def __hash__(self):
        return hash(self.getValues())

    @staticmethod
    def fromId(id):
        for material in Material:
            if material.getId() == id:
                return material
        return None

class MeleeWeapon:
    def __init__(self, material, damage, reach):
        self.material = material
        self.damage = damage
        self.reach = reach

    def getType(self):
        return self.material

class Tools:
    tools = {
        Material.PICKAXE: 0,
        Material.EXPLOSIVE_PICKAXE: 3
    }

class Weapons:
    weapons = {
        Material.SWORD: MeleeWeapon(Material.SWORD, 5, 2),
        Material.FIRE_SWORD: MeleeWeapon(Material.FIRE_SWORD, 7, 3),
        Material.ICE_SWORD: MeleeWeapon(Material.ICE_SWORD, 6, 3)
    }
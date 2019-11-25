from game.world.block import Block
from game.item.material import Material
from game.item.item import ItemStack

# Stores useful global constants
class Constants:
    WORLD_HEIGHT = 101
    WORLD_WIDTH = 201
    SEED_MAX = (1 << 16) - 1

    BLOCK_SIZE = 10

    DEFAULT_WIDTH = 30
    DEFAULT_HEIGHT = 10
    TEXT_COLOR = (0, 0, 0)
    FPS = 60

    WALK_FACTOR = 3
    JUMP_FACTOR = 0.2
    GRAVITY = 0.2

    AIR_BLOCK = Block(Material.AIR, 0, 0)
    EMPTY_ITEM = ItemStack(Material.AIR, 1)

    INVENTORY_WIDTH = 9
    INVENTORY_HEIGHT = 5
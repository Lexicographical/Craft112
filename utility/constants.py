from game.world.block import Block, Blocks

class Constants:
    WORLD_HEIGHT = 101
    WORLD_WIDTH = 101

    DEFAULT_WIDTH = 30
    DEFAULT_HEIGHT = 10
    TEXT_COLOR = (0, 0, 0)
    FPS = 60

    SPRITE_COUNT = -1
    WALK_FACTOR = 3
    JUMP_FACTOR = 0.1

    AIR_BLOCK = Block(Blocks.AIR, 0, 0)
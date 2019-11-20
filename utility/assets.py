import pygame
from utility.constants import Constants
from game.world.material import Material

class Assets:
    assets = {}

    @staticmethod
    def loadAssets():
        assets = {}
        assets["spriteLeft"] = [
            Assets.loadImage(f"L{i}.png")
            for i in range(1, 10)
        ]
        assets["spriteRight"] = [
            Assets.loadImage(f"R{i}.png")
            for i in range(1, 10)
        ]
        Constants.SPRITE_COUNT = len(assets["spriteLeft"])
        assets["sprite"] = Assets.loadImage("standing.png")
        assets["background"] = Assets.loadImage("background.jpg", transparent=False)

        assets["blocks"] = [
            Assets.loadImage(f"block_{i}.png", folder="blocks", transparent=False)
            for i in range(len(Material))
        ]
        assets["blocks"][0] = Assets.loadImage("block_0.png", folder="blocks")

        Assets.assets = assets

    @staticmethod
    def loadImage(file, folder="", transparent=True):
        if folder != "":
            folder += "/"
        path = f"assets/images/{folder}{file}"
        if transparent:
            return pygame.image.load(path).convert_alpha()
        else:
            return pygame.image.load(path).convert()

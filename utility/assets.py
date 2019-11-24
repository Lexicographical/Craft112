import pygame
from utility.constants import Constants
from game.item.material import Material

class Assets:
    assets = {}

    @staticmethod
    def loadAssets():
        assets = {}
        assets["spriteLeft"] = [
            Assets.loadImage(f"L{i}.png", folder="entity")
            for i in range(1, 10)
        ]
        assets["spriteRight"] = [
            Assets.loadImage(f"R{i}.png", folder="entity")
            for i in range(1, 10)
        ]
        Constants.SPRITE_COUNT = len(assets["spriteLeft"])
        assets["sprite"] = Assets.loadImage("standing.png", folder="entity")
        assets["background"] = Assets.loadImage("background.jpg", transparent=False)

        assets["textures"] = {}

        for material in Material:
            try:
                id = material.value
                img = Assets.loadImage(f"{id}.png", folder="material", transparent=False)
                assets["textures"][id] = img
            except:
                print(f"Could not open {id}.png")

        assets["textures"][0] = Assets.loadImage("0.png", folder="material")

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

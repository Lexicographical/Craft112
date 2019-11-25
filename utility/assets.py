import pygame
from utility.constants import Constants
from game.item.material import Material

# Utility file for loading assets in the game
class Assets:
    assets = {}

    # TODO: make connecting background
    @staticmethod
    def loadAssets(app):
        assets = {}
        assets["playerLeft"] = [
            Assets.loadImage(f"L{i}.png", folder="entity")
            for i in range(1, 10)
        ]
        assets["playerRight"] = [
            Assets.loadImage(f"R{i}.png", folder="entity")
            for i in range(1, 10)
        ]

        assets["player"] = Assets.loadImage("standing.png", folder="entity")

        assets["enemyLeft"] = [
            Assets.loadImage(f"L{i}E.png", folder="entity")
            for i in range(1, 9)
        ]
        assets["enemyRight"] = [
            Assets.loadImage(f"R{i}E.png", folder="entity")
            for i in range(1, 9)
        ]
        assets["enemy"] = assets["enemyLeft"][0]

        assets["background"] = Assets.loadImage("background.png", transparent=False)
        assets["background"] = pygame.transform.scale(assets["background"], (960, 540))

        assets["textures"] = {}

        for material in Material:
            try:
                id, transparent = material.getValues()
                img = Assets.loadImage(f"{id}.png", folder="material", transparent=transparent)
                assets["textures"][id] = img
            except:
                print(f"Could not open {id}.png")

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

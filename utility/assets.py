import pygame

class Assets:
    assets = {}

    @staticmethod
    def loadAssets():
        assets = {}
        assets["spriteLeft"] = [
            Assets.loadImage("images", f"L{i}.png")
            for i in range(1, 10)
        ]
        assets["spriteRight"] = [
            Assets.loadImage("images", f"R{i}.png")
            for i in range(1, 10)
        ]
        assets["sprite"] = Assets.loadImage("images", "standing.png")

        Assets.assets = assets

    @staticmethod
    def loadImage(folder, file, transparent=True):
        path = f"assets/{folder}/{file}"
        if transparent:
            return pygame.image.load(path).convert_alpha()
        else:
            return pygame.image.load(path).convert()

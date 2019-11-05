import pygame
from components.button import Button
from components.clickable import Clickable
from components.label import Label
from game.entity.player import Player
from scenes.scene import Scene
from utility.assets import Assets
from utility.colors import Colors
from utility.fonts import Fonts

# TODO: implement sprites through built-in sprite class
# use groups

class GameScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        width, height = self.app.width, self.app.height
        self.player = Player()
        self.player.position = [width/2, height/2]

        self.right = False
        self.left = False
        self.walkTick = 0

        self.jump = False
        self.jumpTick = 10

        self.initComponents()

    def initComponents(self):
        pass

# Cite https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-animation/
# or change code
    def drawComponents(self):
        window = self.app.window
        player = self.player
        px, py = player.position
        assets = Assets.assets

        rect = pygame.Rect(px, py, 10, 30)
        rect.center = (px, py)

        if self.left:
            window.blit(assets["spriteLeft"][self.walkTick//3], rect)
            self.walkTick += 1
        elif self.right:
            window.blit(assets["spriteRight"][self.walkTick//3], rect)
            self.walkTick += 1
        else:
            window.blit(assets["sprite"], rect)
            self.walkTick += 1

        if self.walkTick >= 26:
            self.walkTick = 0

    def onKeyPress(self, keys, mods):
        super().onKeyPress(keys, mods)
        if keys[pygame.K_a]:
            self.left = True
            self.right = False
            self.player.movePlayer(-1, 0)
        elif keys[pygame.K_d]:
            self.right = True
            self.left = False
            self.player.movePlayer(1, 0)
        else:
            self.left = False
            self.right = False
            self.walkTick = 0

        if self.jump:
            if self.jumpTick >= -10:
                sign = 1 if self.jumpTick < 0 else -1
                jumpFactor = 0.1
                dy = (self.jumpTick ** 2) * jumpFactor * sign
                self.player.movePlayer(0, dy)
                self.jumpTick -= 1
            else:
                self.jump = False
                self.jumpTick = 10
        else:
            if keys[pygame.K_SPACE]:
                self.jump = True
                self.left = False
                self.right = False
                self.walkTick = 0

    def onMouseClick(self, mousePos):
        for component in self.components:
            if (isinstance(component, Clickable) and 
                component.isClicked(mousePos)):
                component.click()

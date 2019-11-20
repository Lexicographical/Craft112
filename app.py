import pygame
from pygame.locals import *
from scenes.main_menu_scene import MainMenuScene
from scenes.game_scene import GameScene
from utility.constants import Constants
from utility.assets import Assets

class App:
    TITLE = "Craft 112"

    def __init__(self, width=640, height=400):
        self.running = False
        self.width, self.height = width, height
        self.scenes = {}
        self.activeScene = None
        self.window = None
        self.clock = pygame.time.Clock()

    def initialize(self):
        pygame.init()
        self.window = pygame.display.set_mode(
                    (self.width, self.height))
        pygame.display.set_caption(App.TITLE)
        Assets.loadAssets()
        self.initializeScenes()
        self.changeScene("main")
        self.running = True

    def initializeScenes(self):
        self.scenes = {
            "main": MainMenuScene(self),
            "game": GameScene(self)
        }

    def changeScene(self, sceneName):
        self.activeScene = self.scenes[sceneName]

    def onEvent(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.activeScene.onMouseClick(event.pos)

    def onKeyPress(self, keys, mods):
        self.activeScene.onKeyPress(keys, mods)
 
    def onDraw(self):
        if self.activeScene is not None:
            self.activeScene.drawComponents()

    def start(self):
        self.initialize()
        while self.running:
            self.window.fill((255, 255, 255))

            keys = pygame.key.get_pressed()
            mods = pygame.key.get_mods()
            self.onKeyPress(keys, mods)

            for event in pygame.event.get():
                self.onEvent(event)

            self.onDraw()
            pygame.display.update()
            self.clock.tick(Constants.FPS)
        pygame.quit()

    def quit(self):
        self.running = False
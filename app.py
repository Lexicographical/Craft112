import pygame
from pygame.locals import *
from scenes.main_menu_scene import MainMenuScene
from scenes.game_scene import GameScene
from scenes.load_world_scene import LoadWorldScene
from utility.constants import Constants
from utility.assets import Assets
from threading import Thread
import sys

# Root app for starting the game
class App:
    TITLE = "Craft 112"

    def __init__(self, width=640, height=480):
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
        Assets.loadAssets(self)
        self.initializeScenes()
        self.changeScene("main")
        self.running = True

        self.volumeOn = True
        self.musicChannel = pygame.mixer.Channel(0)

    def initializeScenes(self):
        self.scenes = {
            "main": MainMenuScene(self),
            "game": GameScene(self),
            "load_game": LoadWorldScene(self)
        }

    def changeScene(self, sceneName):
        self.activeScene = self.scenes[sceneName]
        if sceneName == "game" and self.activeScene.isPaused:
            self.activeScene.togglePause()

    def onEvent(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.activeScene.onMouseClick(event.pos)
            if event.button == 3:
                self.activeScene.onMouseRightClick(event.pos)
            elif event.button in [4, 5]:
                scroll = 1 if event.button == 4 else -1
                self.activeScene.onMouseScroll(scroll)
        if event.type == pygame.KEYDOWN:
            key = event.key
            self.onKeyDown(key)
        if event.type == pygame.MOUSEMOTION:
            self.activeScene.onMouseMove(pygame.mouse.get_pos())

    def onKeyPress(self, keys, mods):
        self.activeScene.onKeyPress(keys, mods)

    def onKeyDown(self, key):
        self.activeScene.onKeyDown(key)
 
    def onDraw(self):
        if self.activeScene is not None:
            self.activeScene.drawComponents()

    def onTick(self):
        if self.activeScene is not None:
            self.activeScene.onTick()

    def start(self):
        self.initialize()
        self.playMusic()
        while self.running:
            self.window.fill((255, 255, 255))

            keys = pygame.key.get_pressed()
            mods = pygame.key.get_mods()
            self.onKeyPress(keys, mods)

            for event in pygame.event.get():
                self.onEvent(event)

            self.onDraw()
            self.onTick()
            pygame.display.update()
            self.clock.tick(Constants.FPS)
        pygame.quit()

    def quit(self):
        self.running = False

    def playMusic(self):
        soundtrack = pygame.mixer.Sound("assets/sounds/soundtrack.ogg")
        self.musicChannel.set_volume(1)
        thread = Thread(target=lambda: 
            self.musicChannel.play(soundtrack, loops=-1))
        thread.start()

if __name__ == "__main__":
    app = App()
    app.start()
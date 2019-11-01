import pygame
from pygame.locals import *
from scenes.main_menu import MainMenuScene

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
                    (self.width, self.height),
                    pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption(App.TITLE)
        self.initializeScenes()
        self.changeScene("main")
        self.running = True

    def initializeScenes(self):
        self.scenes = {
            "main": MainMenuScene(self)
        }

    def changeScene(self, sceneName):
        self.activeScene = self.scenes[sceneName]

    def onEvent(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            self.activeScene.onKeyPress(pygame.key.name(event.key), event.mod)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.activeScene.onMouseClick(event.pos)
        # TODO: handle mouse click
 
    def onDraw(self):
        if self.activeScene is not None:
            self.activeScene.drawComponents()

    def start(self):
        self.initialize()
        while self.running:
            self.window.fill((255, 255, 255))
            for event in pygame.event.get():
                self.onEvent(event)
            self.onDraw()
            pygame.display.update()
            self.clock.tick(15)
        pygame.quit()

    def quit(self):
        self.running = False
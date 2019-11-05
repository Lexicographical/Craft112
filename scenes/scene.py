import pygame

class Scene:
    def __init__(self, app):
        self.app = app
        self.components = set()

    def addComponent(self, component):
        self.components.add(component)

    def addComponents(self, components):
        for component in components:
            self.addComponent(component)

    def drawComponents(self):
        for component in self.components:
            component.draw()

    def onKeyPress(self, keys, mods):
        if keys[pygame.K_q] and (mods & pygame.KMOD_CTRL):
            self.app.quit()

    def onMouseClick(self, mousePos):
        pass
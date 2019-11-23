import pygame
from components.component import Component

# Top-level class for scenes in the game
class Scene:
    def __init__(self, app):
        self.app = app
        self.components = set()

    def addComponent(self, component):
        self.components.add(component)

    def addComponents(self, components):
        for component in components:
            assert(isinstance(component, Component))
            self.components.add(component)

    def removeComponent(self, component):
        if component in self.components:
            self.components.remove(component)

    def drawComponents(self):
        for component in self.components:
            component.draw()

    def onKeyPress(self, keys, mods):
        if keys[pygame.K_q] and (mods & pygame.KMOD_CTRL):
            self.app.quit()

    def onMouseClick(self, mousePos): pass
    def onMouseScroll(self, scroll): pass
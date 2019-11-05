import pygame
from components.component import Component
from utility.constants import Constants


class Label(Component):
    def __init__(self, window, x, y, text, font, color=Constants.TEXT_COLOR,
                 background=None):
        super().__init__(window, x, y)
        self.text = text
        self.font = font
        self.color = color
        self.background = background
        self.label = self.font.render(self.text, True, self.color,
                                      self.background)

    def draw(self):
        label = self.label
        rect = label.get_rect()
        rect.center = (self.x, self.y)
        self.window.blit(label, rect)

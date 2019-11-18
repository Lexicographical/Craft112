import uuid
import pygame
from utility.constants import Constants

# Top level class for UI components
class Component:
    def __init__(self, window, x, y, width=Constants.DEFAULT_WIDTH,
            height=Constants.DEFAULT_HEIGHT,
            fillColor=None, borderColor=None, borderWidth=0):
        self.type = "Component"
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fillColor = fillColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth

        self.uuid = uuid.uuid4()
    
    def draw(self):
        rect = self.getBoundingRect()
        if self.fillColor is not None:
            pygame.draw.rect(self.window, self.fillColor, rect)
        if self.borderWidth > 0 and self.borderColor is not None:
            pygame.draw.rect(self.window, self.borderColor, rect,
                             self.borderWidth)

    def getBoundingRect(self):
        x, y = self.x, self.y
        width, height = self.width, self.height

        rect = pygame.Rect(x, y, width, height)
        rect.center = x, y

        return rect

    def __hash__(self):
        return hash((self.x, self.y, self.width, self.height, self.uuid))

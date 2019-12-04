import pygame
from components.label import Label
from utility.constants import Constants

# Top level class for clickable components. Not an actual component on its own
class Clickable:
    def __init__(self, x, y, width=Constants.DEFAULT_WIDTH,
                 height=Constants.DEFAULT_WIDTH):
        self.type = "Clickable"
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onClickListener = lambda: print("Clicked")

    def setOnClickListener(self, fn, args=None):
        self.onClickListener = fn
        self.args = args

    def click(self):
        if self.args is not None:
            self.onClickListener(self.args)
        else:
            self.onClickListener()

    def isClicked(self, mousePos):
        mx, my = mousePos
        rect = self.getBoundingRect()
        return rect.collidepoint((mx, my))

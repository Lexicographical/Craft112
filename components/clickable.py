import pygame
from components.label import Label
from utility.constants import Constants


class Clickable():
    def __init__(self, x, y, width=Constants.DEFAULT_WIDTH,
                 height=Constants.DEFAULT_WIDTH):
        self.type = "Clickable"
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onClickListener = lambda: print("Clicked")

    def setOnClickListener(self, fn):
        self.onClickListener = fn

    def click(self):
        self.onClickListener()

    def isClicked(self, mousePos):
        mx, my = mousePos
        rect = self.getBoundingRect()
        return rect.collidepoint((mx, my))

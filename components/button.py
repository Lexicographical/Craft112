from components.clickable import Clickable
from components.label import Label
from components.component import Component
from utility.constants import Constants

class Button(Clickable, Component):
    def __init__(self, window, x, y,
                 width=Constants.DEFAULT_WIDTH,
                 height=Constants.DEFAULT_HEIGHT,
                 fillColor=None, borderColor=(0, 0, 0),
                 borderWidth=1, text=None, font=None,
                 textColor=(0, 0, 0),):
        Component.__init__(self, window, x, y, width=width, height=height,
            fillColor=fillColor, borderColor=borderColor,
            borderWidth=borderWidth)
        Clickable.__init__(self, x, y, width=width, height=height)
        self.type = "Button"
        self.font = font
        self.textColor = textColor
        self.label = None

        if text is not None:
            self.label = Label(self.window, self.x, self.y, text, self.font,
                               color=self.textColor)
            rect = self.label.label.get_rect()
            self.width, self.height = rect.width, rect.height

    def draw(self):
        super().draw()
        if self.label is not None:
            self.label.draw()
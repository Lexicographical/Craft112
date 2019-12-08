from components.clickable import Clickable
from components.component import Component
from components.label import Label
from components.button import Button
from utility.constants import Constants

# Button that supports images
class ImageButton(Button):
    def __init__(self, window, x, y, image,
                 width=Constants.DEFAULT_WIDTH,
                 height=Constants.DEFAULT_HEIGHT,
                 fillColor=None,
                 borderWidth=1, padding=0):
        Button.__init__(self, window, x, y, fillColor=fillColor,
                borderWidth=borderWidth)
        self.type = "ImageButton"
        self.padding = padding
        self.image = image
        self.width, self.height = image.get_size()

    def draw(self):
        if not self.isEnabled: return
        super().draw()
        rect = super().getBoundingRect()
        self.window.blit(self.image, rect)

    def setImage(self, image):
        self.image = image
        self.width, self.height = image.get_size()

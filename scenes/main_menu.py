from scenes.scene import Scene
from components.label import Label
from components.button import Button
from components.clickable import Clickable
from utility.fonts import Fonts
from utility.colors import Colors
import pygame

class MainMenuScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.initComponents()

    def initComponents(self):
        textFont = pygame.font.Font(Fonts.Courier, 30)
        window = self.app.window
        height, width = self.app.height, self.app.width
        title = Label(window, width/2, height/3,
                            font=textFont, text="Craft112")
        startGame = Button(window, width/2, 2*height/3,
                            font=textFont, text="Start Game")
        # quitGame = Button(window, width/2, 2.5*height/3,
        #                     font=textFont, text="Quit Game")
        
        self.addComponents([title, startGame])

    def onKeyPress(self, key, modifier):
        if key == "q" and (modifier & pygame.KMOD_CTRL):
            self.app.quit()

    def onMouseClick(self, mousePos):
        print(mousePos)
        for component in self.components:
            if (isinstance(component, Clickable) and 
                component.isClicked(mousePos)):
                component.click()
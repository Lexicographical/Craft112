import pygame
from components.button import Button
from components.label import Label
from scenes.scene import Scene
from utility.colors import Colors
from utility.fonts import Fonts

# TODO: use pygame mixer to play sounds: https://www.pygame.org/docs/ref/mixer.html
# Scene to display the main menu
class MainMenuScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.initComponents()

    def initComponents(self):
        textFont = pygame.font.Font(Fonts.Courier, 30)
        window = self.app.window
        height, width = self.app.height, self.app.width
        title = Label(window, width/2, 0.5*height/3,
                            font=textFont, text="Craft112")
            
        startGame = Button(window, width/2, 1.5*height/3,
                            font=textFont, text="Start Game",
                            padding=10)
        startGame.setOnClickListener(lambda: self.app.changeScene("game"))
        
        quitGame = Button(window, width/2, 2*height/3,
                            font=textFont, text="Quit Game",
                            padding=10)
        quitGame.setOnClickListener(self.app.quit)

        self.addComponents([title, startGame, quitGame])

    def onKeyPress(self, keys, mods):
        super().onKeyPress(keys, mods)
        if keys[pygame.K_RETURN]:
            self.app.changeScene("game")

    def onMouseClick(self, mousePos):
        super().onMouseClick(mousePos)

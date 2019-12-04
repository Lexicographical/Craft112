import pygame
from components.button import Button
from components.label import Label
from scenes.scene import Scene
from utility.colors import Colors
from utility.fonts import Fonts
from utility.assets import Assets

# Scene to display the main menu
class MainMenuScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.initComponents()

    def initComponents(self):
        textFont = Fonts.getFont(Fonts.Courier, 30)
        window = self.window
        height, width = self.app.height, self.app.width
        title = Label(window, width/2, 1*height/3,
                            font=textFont, text="Craft112")
            
        startGame = Button(window, width/2, 1.5*height/3,
                            font=textFont, text="Start Game",
                            padding=10)
        startGame.setOnClickListener(lambda: self.app.changeScene("load_game"))

        quitGame = Button(window, width/2, 2*height/3,
                            font=textFont, text="Quit Game",
                            padding=10)
        quitGame.setOnClickListener(self.app.quit)

        self.addComponents([title, startGame, quitGame])

    def drawComponents(self):
        self.drawBackground()
        super().drawComponents()

    def drawBackground(self):
        window = self.window
        bg = Assets.assets["background"]
        window.blit(bg, (0, 0))

    def onKeyPress(self, keys, mods):
        super().onKeyPress(keys, mods)
import pygame
from components.button import Button
from components.label import Label
from scenes.scene import Scene
from utility.colors import Colors
from utility.fonts import Fonts
from utility.assets import Assets
from utility.utility import Utility
from components.imagebutton import ImageButton

# Scene that displays the world selection screen
class LoadWorldScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.initComponents()
        self.worlds = Utility.loadWorlds()
        self.updateButtons()

    def initComponents(self):
        textFont = Fonts.getFont(Fonts.Courier, 30)
        window = self.window
        height, width = self.app.height, self.app.width
        title = Label(window, width/2, 0.5*height/3,
                            font=textFont, text="Load World")

        self.worldButtons = []
        y = [1.8, 2.5, 3.2]
        for i in range(3):
            button = Button(window, width/2, y[i]*height/4,
                            font=textFont, text="New World",
                            padding=10, fillColor=Colors.WHITE)
            button.setOnClickListener(self.loadWorld, i)
            self.worldButtons.append(button)

        self.deleteButtons = []
        for i in range(3):
            button = self.worldButtons[i]
            imgButton = ImageButton(window, width/2 + button.width, y[i]*height/4,
                                 Assets.assets["delete"], padding=10, borderWidth=0)
            imgButton.setOnClickListener(self.deleteWorld, i)
            self.deleteButtons.append(imgButton)

        self.addComponents(self.worldButtons)
        self.addComponents(self.deleteButtons)
        self.addComponent(title)

    def drawComponents(self):
        self.drawBackground()
        super().drawComponents()

    def drawBackground(self):
        window = self.window
        bg = Assets.assets["background"]
        window.blit(bg, (0, 0))

    def updateButtons(self):
        for i in range(3):
            worldButton = self.worldButtons[i]
            worldName = "New World"
            world = self.worlds[i]
            if world is not None:
                worldName = world.name
            worldButton.setText(worldName)

    def loadWorld(self, i):
        gameScene = self.app.scenes["game"]
        if self.worlds[i] is not None:
            gameScene.world = self.worlds[i]
            gameScene.player = self.worlds[i].player
        else:
            gameScene.initNew()
            gameScene.world.name = f"World {i+1}"
            self.worlds[i] = gameScene.world
        self.app.changeScene("game")
        self.updateButtons()

    def deleteWorld(self, i):
        Utility.deleteWorld(i+1)
        self.worlds[i] = None
        self.updateButtons()

    def onKeyDown(self, key):
        if key == pygame.K_ESCAPE:
            self.app.changeScene("main")
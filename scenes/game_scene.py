import math
import pygame
from components.button import Button
from components.clickable import Clickable
from components.label import Label
from game.entity.player import Player
from game.world.world import World
from scenes.scene import Scene
from utility.assets import Assets
from utility.colors import Colors
from utility.constants import Constants
from utility.fonts import Fonts

# Scene to display the gameplay
class GameScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.initGame()
        self.initComponents()

    def initGame(self):
        self.world = World()
        self.world.generateWorld()
        self.player = Player()
        self.player.position = [0, 0]

        self.previewWidth = 10
        self.blockSize = self.app.width / (self.previewWidth * 2 + 1)
        self.previewHeight = math.ceil(self.app.height / self.blockSize)
        print(self.previewWidth, self.previewHeight, self.blockSize)

    def initComponents(self):
        textFont = pygame.font.Font(Fonts.Courier, 30)
        self.label = Label(self.app.window, 0, 0, text="(0, 0)", font=textFont)
        rect = self.label.label.get_rect()
        width, height = rect.width, rect.height
        self.label.x = width
        self.label.y = height/2
        self.addComponent(self.label)

# Cite https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-animation/
# or change code
    def drawComponents(self):
        self.drawBackground()
        self.drawWorld()
        self.drawPlayer()

        super().drawComponents()

    def drawBackground(self):
        window = self.app.window
        player = self.player
        bg = Assets.assets["background"]
        bgSize = bg.get_size()
        windowSize = window.get_size()
        coord = [windowSize[i] - bgSize[i] - player.position[i] for i in range(2)]
        window.blit(bg, coord)

    # TODO: preview positioning is not working properly
    # blocks are not in the right position. fix
    def drawWorld(self):
        world = self.world
        height, width = self.previewHeight, self.previewWidth
        player = self.player
        px, py = player.position
        offset = 5 # load outside canvas to make buffering less evident
        # print(-py-height, -py+height+offset)
        for y in range(-height-offset, height+offset):
            for x in range(-width-offset, width+offset):
                bx = x + px
                by = y - py
                block = world.getBlock((bx, by))

                size = self.blockSize
                renderX = (x+width - (abs(px)%1)) * size
                renderY = (y+height - (abs(py)%1)) * size
                self.drawBlock(block, (renderX, renderY))

    def drawBlock(self, block, position):
        window = self.app.window
        texture = Assets.assets["blocks"][block.getId()]
        
        x, y = position
        size = self.blockSize
        blockRect = pygame.Rect(0, 0, size, size)
        blockRect.center = (x + size/2, y + size/2)

        window.blit(texture, blockRect)

    def drawPlayer(self):
        window = self.app.window
        cx, cy = self.app.width / 2, self.app.height / 2
        assets = Assets.assets
        player = self.player

        self.label.setText(player.getPosition())

        # create rect for sprite location
        width, height = assets["sprite"].get_size()
        spriteRect = pygame.Rect(0, 0, width, height)
        spriteRect.center = (cx, cy)

        # animate sprite walk every other WALK_FACTOR ticks
        spriteIndex = player.walkTick // Constants.WALK_FACTOR
        if player.left:
            window.blit(assets["spriteLeft"][spriteIndex], spriteRect)
        elif player.right:
            window.blit(assets["spriteRight"][spriteIndex], spriteRect)
        else:
            window.blit(assets["sprite"], spriteRect)
        player.walkTick += 1

        spriteCount = Constants.SPRITE_COUNT
        if player.walkTick >= spriteCount * Constants.WALK_FACTOR:
            player.walkTick = 0

    def onKeyPress(self, keys, mods):
        super().onKeyPress(keys, mods)
        player = self.player

        if keys[pygame.K_a]:
            player.move(-1, 0, walk=True)
        elif keys[pygame.K_d]:
            player.move(1, 0, walk=True)
        elif keys[pygame.K_w]:
            player.move(0, 1)
        elif keys[pygame.K_s]:
            player.move(0, -1)
        else:
            player.faceDirection(0, 0)

        if not player.isJumping and keys[pygame.K_SPACE]:
            player.jump()
        
        player.update()

    def onMouseClick(self, mousePos):
        for component in self.components:
            if (isinstance(component, Clickable) and 
                component.isClicked(mousePos)):
                component.click()

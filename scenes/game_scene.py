import math
import pygame
from pygame.color import Color
from components.button import Button
from components.label import Label
from game.entity.player import Player
from game.item.item import *
from game.item.material import Material
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

        self.isPaused = False

    def initGame(self):
        self.world = World()
        self.world.generateWorld()
        self.initPlayer()

        y = self.world.getHighestBlock(0)
        print("Highest block", y)
        self.player.position = [0, y]

        self.previewWidth = 10
        self.blockSize = self.app.width / (self.previewWidth * 2 + 1)
        self.previewHeight = math.ceil(self.app.height / self.blockSize)

        self.offset = 5 # load outside canvas to hide buffering
        self.renderOffset = 7.5
        self.spawnTickRate = 10
        self.tick = 0

    def initPlayer(self):
        self.player = Player(self.world)
        sword = ItemStack(Material.SWORD, 1)
        pickaxe = ItemStack(Material.PICKAXE, 1)

        self.player.getInventory().addItem(sword)
        self.player.getInventory().addItem(pickaxe)

    def initComponents(self):
        textFont = pygame.font.Font(Fonts.Courier, 30)
        self.label = Label(self.app.window, 0, 0, text="(0, 0)", font=textFont)
        rect = self.label.label.get_rect()
        width, height = rect.width, rect.height
        self.label.x = self.app.width - width
        self.label.y = height/2
        self.addComponent(self.label)

        window = self.app.window
        width, height = self.app.width, self.app.height

        resume = Button(window, width/2, 1.5*height/3,
                            font=textFont, text="Resume Game",
                            fillColor=Color(255, 255, 255),
                            padding=10)
        resume.setOnClickListener(self.togglePause)

        quit = Button(window, width/2, 2*height/3,
                            font=textFont, text="Quit Game",
                            fillColor=Color(255, 255, 255),
                            padding=10)
        quit.setOnClickListener(self.app.quit)

        resume.setEnabled(False)
        quit.setEnabled(False)
        self.pauseComponents = [resume, quit]
        self.addComponents(self.pauseComponents)

    def drawComponents(self):
        self.drawBackground()
        self.drawTerrain()
        self.drawEntities()
        self.drawPlayer()
        self.drawInventory()
        self.drawEquipped()
        self.drawPause()

        super().drawComponents()

    def drawBackground(self):
        window = self.app.window
        player = self.player
        bg = Assets.assets["background"]
        bgSize = bg.get_size()
        windowSize = window.get_size()
        coord = [windowSize[i] - bgSize[i] - player.position[i] for i in range(2)]
        x, y = coord
        width, height = bgSize
        window.blit(bg, coord)
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if (dx != dy) and ((dx == 0) or (dy == 0)):
                    x += width*dx
                    y += height*dy
                    window.blit(bg, (x, y))
                    x -= width*dx
                    y -= height*dy

    def drawTerrain(self):
        world = self.world
        height, width = self.previewHeight, self.previewWidth
        player = self.player
        px, py = player.position
        offset = self.offset
        renderOffset = self.renderOffset
        
        size = self.blockSize
        for y in range(-height-offset, height+offset):
            for x in range(-width-offset, width+offset):
                bx = px + x
                by = py - y
                block = world.getBlock((bx, by))

                renderX = (x+width - abs(px)%1) * size
                renderY = (y+height-renderOffset - abs(py)%1) * size
                self.drawBlock(block, (renderX, renderY))

    def drawBlock(self, block, position):
        window = self.app.window
        texture = Assets.assets["textures"][block.getType().getId()]
        
        x, y = position
        size = self.blockSize
        blockRect = pygame.Rect(0, 0, size, size)
        blockRect.center = (x + size/2, y + size/2)

        window.blit(texture, blockRect)

    def drawPlayer(self):
        window = self.app.window
        cx, cy = self.app.width / 2, self.app.height / 2
        player = self.player
        player.draw(window, cx, cy)

        self.label.setText(player.getPosition())

    def drawEntities(self):
        window = self.app.window
        world = self.world
        px, py = self.player.position
        cx, cy = self.app.width/2, self.app.height/2

        for entity in world.entities:
            x, y = entity.position
            rx = cx + (x - px) * self.blockSize
            ry = cy + (-y + py) * self.blockSize
            entity.draw(window, rx, ry)
            # print(x, y, rx, ry)
        # print()

    def drawInventory(self):
        window = self.app.window
        inventory = self.player.getInventory()
        width = inventory.getDimensions()[0]

        cellSize = 40
        offset = 10
        for i in range(width):
            rect = pygame.Rect(i * cellSize + offset, offset, cellSize, cellSize)
            borderWidth = 1
            if i == self.player.equipIndex:
                borderWidth = 3
            pygame.draw.rect(self.app.window, Color(0, 0, 0), rect, borderWidth)
            
            item = inventory[0][i]
            if item.getType() != Material.AIR:
                id = item.getType().getId()
                texture = Assets.assets["textures"][id]
                window.blit(texture, rect)
  
    # TODO: implement
    def drawEquipped(self):
        pass

    def onKeyPress(self, keys, mods):
        super().onKeyPress(keys, mods)
        if self.isPaused: return
        player = self.player

        if keys[pygame.K_a]:
            player.move(-1, 0, walk=True)
        elif keys[pygame.K_d]:
            player.move(1, 0, walk=True)
        else:
            player.faceDirection(0, 0)
        player.update()

    def onKeyDown(self, key):
        if key == pygame.K_ESCAPE:
            self.togglePause()

        if self.isPaused: return
        player = self.player
        if key == pygame.K_c:
            self.world.rngSpawnEntity(self.player, spawn=True)
        else:
            for i in range(9):
                if key == pygame.K_1 + i:
                    player.equipIndex = i
                    break
        if not player.isJumping and key == pygame.K_SPACE:
            player.jump()
        player.update()

    def onMouseClick(self, mousePos):
        super().onMouseClick(mousePos)
        item = self.player.getEquippedItem()

        if item.getType() == Material.PICKAXE:
            block, bx, by = self.getBlockFromMousePos(mousePos)
            x, y = block.getPosition()
            print("Removing", (bx, by), (x, y))
            self.world.setBlock(Material.AIR, (bx, by))

    # TODO: improve accuracy
    def getBlockFromMousePos(self, mousePos):
        rx, ry = mousePos
        px, py = self.player.position
        size = self.blockSize
        height, width = self.previewHeight, self.previewWidth

        x = rx/size + (abs(px) % 1) - width
        y = ry/size + (abs(py) % 1) - height + self.renderOffset

        bx = px + x
        by = py - y
        print(x, y, bx, by)
        block = self.world.getBlock((bx, by))
        return block, bx, by

    def onMouseScroll(self, scroll):
        player = self.player
        inventory = player.getInventory()
        player.equipIndex = (player.equipIndex - scroll) % (inventory.width)

    def onTick(self):
        self.tick += 1
        if self.tick == self.spawnTickRate:
            self.tick = 0
            self.world.rngSpawnEntity(self.player)

    def drawPause(self):
        if self.isPaused:
            filter = pygame.Surface((self.app.width, self.app.height))
            filter.set_alpha(100)
            filter.fill((255, 255, 255))
            self.app.window.blit(filter, (0, 0))

            for component in self.pauseComponents:
                component.setEnabled(True)
        else:
            for component in self.pauseComponents:
                component.setEnabled(False)

    def togglePause(self):
        self.isPaused = not self.isPaused
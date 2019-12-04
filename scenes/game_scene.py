import math
import pygame
from components.button import Button
from components.imagebutton import ImageButton
from components.label import Label
from game.entity.player import Player
from game.entity.enemy import Enemy
from game.item.item import *
from game.item.material import *
from game.world.world import World
from game.world.vector2d import Vector2D
from scenes.scene import Scene
from utility.assets import Assets
from utility.colors import Colors
from utility.constants import Constants
from utility.fonts import Fonts
from utility.utility import Utility

# Scene to display the gameplay
class GameScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.initNew()
        self.initGame()
        self.initComponents()
        self.initOverlay()

        self.isPaused = False

    def initNew(self):
        self.initWorld()
        self.initPlayer()

    def initWorld(self):
        self.world = World()
        self.world.generateWorld()

    def initGame(self):
        self.player = None
        self.previewWidth = 10
        Constants.blockSize = self.app.width / (self.previewWidth * 2 + 1)
        self.previewHeight = math.ceil(self.app.height / Constants.blockSize)

        self.offset = 5 # load outside canvas to hide buffering
        self.renderOffset = 7.6
        self.holdPos = False
        self.holdPosTickThresh = 30
        self.holdPosTick = 0

        self.difficulty = 2
        self.difficultyLabels = ["Peaceful", "Easy", "Normal", "Hard"]

    def initPlayer(self):
        self.player = Player(self.world)
        sword = ItemStack(Material.SWORD, 1)
        pickaxe = ItemStack(Material.PICKAXE, 1)

        self.player.getInventory().addItem(sword)
        self.player.getInventory().addItem(pickaxe)

        y = self.world.getHighestBlock(0)
        self.player.position = Vector2D(0, y)
        self.world.addEntity(self.player)
 
    def initComponents(self):
        textFont = Fonts.getFont(Fonts.Courier, 30)
        self.label = Label(self.window, 0, 0, text="(0, 0)", font=textFont)
        rect = self.label.label.get_rect()
        width, height = rect.width, rect.height
        self.label.x = self.app.width - width
        self.label.y = height/2
        self.label.setEnabled(False)
        self.addComponent(self.label)

    def initOverlay(self):
        textFont = Fonts.getFont(Fonts.Courier, 30)
        window = self.window
        width, height = self.app.width, self.app.height

        unit = height/4

        self.volumeButton = ImageButton(window, 2*width/3, 1.6*unit,
                                  Assets.assets["volume_on"],
                                  fillColor=Colors.WHITE)
        self.volumeButton.setOnClickListener(self.toggleVolume)

        self.respawnButton = Button(window, width/2, 2*unit,
                            font=textFont, text="Respawn",
                            fillColor=Colors.WHITE,
                            padding=10)
        self.respawnButton.setOnClickListener(self.respawnPlayer)

        self.resumeButton = Button(window, width/2, 2*unit,
                            font=textFont, text="Resume Game",
                            fillColor=Colors.WHITE,
                            padding=10)
        self.resumeButton.setOnClickListener(self.togglePause)

        self.difficultyButton = Button(window, width/2, 2.5*unit,
                            font=textFont, text="Difficulty: Normal",
                            fillColor=Colors.WHITE,
                            padding=10)
        self.difficultyButton.setOnClickListener(self.cycleDifficulty)

        self.quitButton = Button(window, width/2, 3*unit,
                            font=textFont, text="Main Menu",
                            fillColor=Colors.WHITE,
                            padding=10)
        self.quitButton.setOnClickListener(self.quit)  

        self.overlayComponents = [self.resumeButton, self.quitButton, self.respawnButton,
                                  self.volumeButton, self.difficultyButton]

        for component in self.overlayComponents:
            component.setEnabled(False)

        self.addComponents(self.overlayComponents)

    def drawComponents(self):
        self.drawBackground()
        self.drawTerrain()
        self.drawEntities()
        self.drawInventory()
        self.drawOverlay()

        super().drawComponents()

    def drawBackground(self):
        window = self.window
        player = self.player
        bg = Assets.assets["gradient"]
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
        
        size = Constants.blockSize
        for y in range(-height-offset, height+offset):
            for x in range(-width-offset, width+offset):
                bx = px + x
                by = py - y
                block = world.getBlock((bx, by))

                renderX = (x+width) * size
                renderY = (y+height-renderOffset) * size
                self.drawBlock(block, (renderX, renderY))

    def drawBlock(self, block, position):
        window = self.window
        texture = Assets.assets["textures"][block.getType().getId()][0]
        
        x, y = position
        size = Constants.blockSize
        blockRect = pygame.Rect(0, 0, size, size)
        blockRect.center = (x + size/2, y + size/2)

        window.blit(texture, blockRect)

    def drawEntities(self):
        self.label.setText(str(self.player.getPosition()))

        window = self.window
        world = self.world
        px, py = self.player.position
        cx, cy = self.app.width/2, self.app.height/2

        for entity in world.entities:
            x, y = entity.position
            rx = cx + (x - px) * Constants.blockSize
            ry = cy + (-y + py) * Constants.blockSize
            if not isinstance(entity, Player):
                ry += self.renderOffset
            entity.draw(window, rx, ry)

    def drawInventory(self):
        window = self.window
        inventory = self.player.getInventory()
        width = inventory.getDimensions()[0]

        cellSize = 40
        offset = 10
        for i in range(width):
            rect = pygame.Rect(i * cellSize + offset, offset, cellSize, cellSize)
            borderWidth = 1
            if i == self.player.equipIndex:
                borderWidth = 3
            pygame.draw.rect(self.window, Colors.BLACK, rect, borderWidth)
            
            item = inventory[0][i]
            if item.getType() != Material.AIR:
                id = item.getType().getId()
                texture = Assets.assets["textures"][id]
                if item.getType() in Tools.tools:
                    texture = texture[0]
                else:
                    texture = texture[1]
                tWidth, tHeight = texture.get_size()
                tRect = pygame.Rect(0, 0, tWidth, tHeight)
                tRect.center = rect.center
                window.blit(texture, tRect)

                amount = item.getAmount()
                self.drawItemCount(amount, tRect)

    def drawItemCount(self, amount, rect):
        font = Fonts.getFont(Fonts.Courier, 20)
        if amount > 1:
            window = self.window
            x, y = rect.bottomright
            countLabel = Label(window, x, y, str(amount), font,
                                color=Colors.BLACK)
            countLabel.draw()
  
    def onKeyPress(self, keys, mods):
        super().onKeyPress(keys, mods)
        if self.isPaused: return
        player = self.player

        if keys[pygame.K_a]:
            player.move(-1, 0, walk=True)
        elif keys[pygame.K_d]:
            player.move(1, 0, walk=True)
        else:
            if not self.holdPos:
                player.faceDirection(0, False)
        player.update()

    def onKeyDown(self, key):
        if key == pygame.K_ESCAPE and self.player.isAlive:
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
        if self.isPaused: return
        item = self.player.getEquippedItem()

        if item.getType() == Material.PICKAXE:
            self.breakBlock(mousePos)
        elif item.getType() == Material.SWORD:
            self.attack(mousePos, item)

    def onMouseRightClick(self, mousePos):
        if self.isPaused: return
        player = self.player
        type = player.getEquippedItem().getType()
        if type not in Tools.tools and type != Material.AIR:
            _, bx, by = self.getBlockFromMousePos(mousePos)
            world = self.world
            item = player.getEquippedItem()
            world.setBlock(item.getType(), (bx, by))
            item.setAmount(item.getAmount() - 1)
            if item.getAmount() == 0:
                item.material = Material.AIR
                item.amount = 1

    def getBlockFromMousePos(self, mousePos):
        rx, ry = mousePos
        px, py = self.player.position
        size = Constants.blockSize
        height, width = self.previewHeight, self.previewWidth
        offset = 0.5

        x = rx/size - width - offset
        y = ry/size - height + self.renderOffset - offset

        bx = px + x
        by = py - y
        block = self.world.getBlock((bx, by))
        return block, bx, by

    def breakBlock(self, mousePos):
        block, bx, by = self.getBlockFromMousePos(mousePos)
        if block.getType() != Material.AIR:
            self.world.setBlock(Material.AIR, (bx, by))
            self.player.getInventory().addItem(ItemStack(block.getType(), 1))

    def attack(self, mousePos, item):
        mx = mousePos[0]
        cx = self.app.width/2
        player = self.player
        direction = 1 if mx > cx else -1

        dead = []
        self.player.faceDirection(direction, False)
        self.holdPos = True

        weapon = Tools.tools[item.getType()]
        damage = weapon.damage
        reach = weapon.reach

        for entity in self.world.entities:
            if isinstance(entity, Enemy):
                pPos = player.position
                ePos = entity.position
                
                px, ex = pPos[0], ePos[0]

                relativeDelta = 1 if ex > px else -1
                distance = pPos.distance(ePos)
                if relativeDelta == direction and distance <= reach:
                    entity.damage(damage, relativeDelta)
                    if not entity.isAlive:
                        dead.append(entity)
        for entity in dead:
            self.world.entities.remove(entity)

    def onMouseScroll(self, scroll):
        player = self.player
        inventory = player.getInventory()
        player.equipIndex = (player.equipIndex - scroll) % (inventory.width)

    def onTick(self):
        if self.isPaused: return
        self.world.tick()
        if self.holdPos:
            self.holdPosTick += 1
            if self.holdPosTick == self.holdPosTickThresh:
                self.holdPosTick = 0
                self.holdPos = False
        if not self.player.isAlive:
            self.isPaused = True

    def drawOverlay(self):
        if Constants.FILTER is None:
            Constants.FILTER = pygame.Surface((self.app.width, self.app.height))
            Constants.FILTER.set_alpha(100)
            Constants.FILTER.fill((255, 255, 255))

        for component in self.overlayComponents:
            enabled = not self.player.isAlive or self.isPaused
            component.setEnabled(enabled)

        if not self.player.isAlive:
            self.window.blit(Constants.FILTER, (0, 0))
            self.resumeButton.setEnabled(False)
        elif self.isPaused:
            self.window.blit(Constants.FILTER, (0, 0))
            self.respawnButton.setEnabled(False)

    def togglePause(self):
        self.isPaused = not self.isPaused
        self.difficulty = self.world.difficulty

    def toggleVolume(self):
        self.app.volumeOn = not self.app.volumeOn
        if self.app.volumeOn:
            self.volume.setImage(Assets.assets["volume_on"])
            self.app.musicChannel.set_volume(1)
        else:
            self.volume.setImage(Assets.assets["volume_off"])
            self.app.musicChannel.set_volume(0)

    def respawnPlayer(self):
        self.player.respawn()
        self.isPaused = False

    def cycleDifficulty(self):
        self.difficulty = (self.difficulty + 1) % 4
        self.world.setDifficulty(self.difficulty)
        self.difficultyButton.setText(f"Difficulty: {self.difficultyLabels[self.difficulty]}")

    def quit(self):
        Utility.save(self.world)
        pygame.event.wait()
        self.app.changeScene("main")
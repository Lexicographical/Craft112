import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type

class Entities:
    PLAYER = "player"
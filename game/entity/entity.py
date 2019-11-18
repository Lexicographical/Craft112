import pygame

# Top level class for game entities
class Entity(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type

# List of all entity types
class Entities:
    PLAYER = "player"
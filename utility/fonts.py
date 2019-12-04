import pygame

# Stores fonts
class Fonts:
    Courier = "assets/fonts/courier.ttf"
    Roboto_Mono = "assets/fonts/roboto_mono.ttf"
    memo = {}

    @staticmethod
    def getFont(fontName, fontSize):
        if fontName not in Fonts.memo:
            Fonts.memo[fontName] = {}
        if fontSize not in Fonts.memo[fontName]:
            Fonts.memo[fontName][fontSize] = pygame.font.Font(fontName, fontSize)
        return Fonts.memo[fontName][fontSize]
from utility.constants import Constants

class Inventory:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = width * height
        self.contents = [[Constants.EMPTY_ITEM] * width for _ in range(height)]

    def addItem(self, itemStack):
        for i in range(self.height):
            for j in range(self.width):
                if self.contents[i][j] == Constants.EMPTY_ITEM:
                    self.contents[i][j] = itemStack
                    return True
        return False

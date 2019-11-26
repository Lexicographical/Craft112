from utility.constants import Constants

# Inventory contains an MxN list of itemstacks
class Inventory:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = width * height
        self.contents = [[Constants.EMPTY_ITEM] * width for _ in range(height)]

    def addItem(self, itemStack):
        for i in range(self.height):
            for j in range(self.width):
                if self.contents[i][j].getType() == itemStack.getType():
                    self.contents[i][j].amount += 1
                    return True
                if self.contents[i][j] == Constants.EMPTY_ITEM:
                    self.contents[i][j] = itemStack
                    return True
        return False

    def getDimensions(self):
        return (self.width, self.height)

    def __getitem__(self, index):
        return self.contents[index]
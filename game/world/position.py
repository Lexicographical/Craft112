class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return str((self.x, self.y))

    def __getitem__(self, index):
        return (self.x, self.y)[index]

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value

    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
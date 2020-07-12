CELL = 64

PLAYER = 'P'
WALL = 'X'
DIAMOND = 'V'
LOCK = 'L'
GREEN_LOCK = 'G'
MESSAGEBOARD = 'M'
ARROW_UP = '^'
ARROW_DOWN = 'v'
ARROW_RIGHT = '>'
ARROW_LEFT = '<'
FRIEND = 'F'
SLIME = 'S'
KEY = 'K'
DOOR = 'D'


class GridMap:
    def __init__(self, conf):
        self.rows = len(conf) + 2  # Add 2 rows for the message board
        self.cols = len(conf[1])
        self.messagePos = 0, self.rows - 2  # Position the message board 2 rows from the bottom
        self.objects = {}

        for y, row in enumerate(conf):
            for x, chr in enumerate(row):
                if chr != ' ':
                    if chr == PLAYER:
                        self.player_col = x
                        self.player_row = y
                        continue

                    self[x, y] = chr

    def width(self):
        return self.cols * CELL

    def height(self):
        return self.rows * CELL

    # Return the x and y of the top left corner
    def xy(self, col, row):
        return col * CELL, row * CELL

    def player_xy(self):
        return self.player_col * CELL, self.player_row * CELL

    def object_in_sight(self):
        col = self.player_col + 1
        row = self.player_row
        while col < self.cols:
            if (col, row) in self.objects:
                obj = self[col, row]
                if obj not in (WALL, PLAYER, MESSAGEBOARD, ARROW_UP, ARROW_DOWN, ARROW_RIGHT, ARROW_LEFT, SLIME, DOOR, KEY):
                    return obj
            col += 1

    def __setitem__(self, key, value):
        self.objects[key] = value

    def __getitem__(self, item):
        if item not in self.objects: return None

        return self.objects[item]

    def __delitem__(self, key):
        del self.objects[key]

    def __iter__(self):
        return self.objects.items().__iter__()

    def rect(self, pos):
        return (self.xy(*pos)[0], self.xy(*pos)[1], CELL, CELL)

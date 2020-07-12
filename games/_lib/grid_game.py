from os.path import join, dirname
from time import sleep
from typing import Iterable

import pygame
from pygame.transform import scale, flip, rotate

from games._lib.grid_map import CELL, WALL, DIAMOND, LOCK, FRIEND, GridMap, GREEN_LOCK, ARROW_DOWN, ARROW_UP, \
    ARROW_LEFT, ARROW_RIGHT, SLIME, DOOR, KEY
from games._lib.objects import Lock, Friend

root = dirname(__file__)

WALL_TILE = pygame.image.load(join(root, "images", "wall.png"))
DIAMOND_TILE = pygame.image.load(join(root, 'images', 'diamond.png'))
PLAYER_TILE = scale(pygame.image.load(join(root, 'images', 'player.png')), (int(CELL * .8), CELL))
PLAYER_TILE_SLIDING = scale(pygame.image.load(join(root, 'images', 'player_sliding.png')), (int(CELL * .8), CELL))
PLAYER_TILE_RED = PLAYER_TILE.copy()
PLAYER_TILE_RED.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)
PLAYER_WON_TILE = scale(pygame.image.load(join(root, 'images', 'player_won.png')), (int(CELL * .8), CELL))
FRIEND_TILE = flip(scale(pygame.image.load(join(root, 'images', 'friend.png')), (int(CELL * .8), CELL)), True, False)
LOCK_TILE = pygame.transform.scale(pygame.image.load(join(root, 'images', 'lock.png')), (64, 64))
GREEN_LOCK_TILE = pygame.transform.scale(pygame.image.load(join(root, 'images', 'lock_green.png')), (64, 64))
ARROW_UP_TILE = scale(pygame.image.load(join(root, 'images', 'arrows.png')), (64, 64))
ARROW_DOWN_TILE = flip(ARROW_UP_TILE.copy(), False, True)
ARROW_LEFT_TILE = rotate(ARROW_UP_TILE.copy(), 90)
ARROW_RIGHT_TILE = rotate(ARROW_UP_TILE.copy(), -90)
KEY_TILE = scale(pygame.image.load(join(root, 'images', 'key.png')), (64, 64))
DOOR_TILE = scale(pygame.image.load(join(root, 'images', 'door.png')), (64, 64))
SLIME_TILE = pygame.transform.scale(pygame.image.load(join(root, 'images', 'slime.png')), (64, 64))
MESSAGEBOARD = 'M'

FPS = 120


class CodingGame:
    def __init__(self, mapdata):
        pygame.init()
        pygame.font.init()

        self.mapdata = mapdata
        self.grid = GridMap(mapdata['map'])
        self.keyboard = mapdata['allowKeyboard']

        self.running = True
        self.won = False
        self.red = False
        self.sliding = False
        self.keys = 0
        self.message = mapdata['welcomeMessage']
        self.font = pygame.font.Font(join(root, "fonts", "ubuntu-regular.ttf"), 26)
        self.clock = pygame.time.Clock()

        self.load_locks()
        self.load_friends()
        self.load_doors()

        self.col, self.row = self.grid.player_col, self.grid.player_row

        # Create a messageboard
        self.messageRect = None
        if self.grid.messagePos is not None:
            mx, my = self.grid.xy(*self.grid.messagePos)
            mw = self.grid.width() - mx
            mh = self.grid.height() - my
            self.messageRect = (mx, my, mw, mh)

        self.screen = pygame.display.set_mode([self.grid.width(), self.grid.height()])
        pygame.display.set_caption(mapdata['title'])

        self._redraw()

    def load_locks(self):
        self.locks = []

        if 'locks' not in self.mapdata:
            return

        for lockdata in self.mapdata['locks']:
            code = lockdata['code']
            if isinstance(code, str):
                lock = Lock(code)
            elif isinstance(code, Iterable):
                lock = Lock(*code)
            else:
                lock = Lock(code)
            if 'label' in lockdata:
                lock.message_in_front = lockdata['label']

            if 'message_wrong_code' in lockdata:
                lock.message_wrong_code = lockdata['message_wrong_code']

            if 'auto_destroys' in lockdata:
                lock.auto_destroys = lockdata['auto_destroys']

            if 'position' in lockdata:
                lock.position = lockdata['position']

            self.locks.append(lock)

    def load_friends(self):
        self.friends = []

        if 'friends' not in self.mapdata:
            return

        for data in self.mapdata['friends']:
            friend = Friend(data['data'], data['message'])
            self.friends.append(friend)

    def load_doors(self):
        self.doors = []

        if 'doors' not in self.mapdata:
            return

        for door in self.mapdata['doors']:
            self.doors.append(door)


    def _redraw(self, player_x=None, player_y=None):
        # This is required so that the app does not appear hanged
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # Cancel redraw if we are not running anymore
        if not self.running:
            return

        # Fill the background
        self.screen.fill((0, 161, 228))

        # Draw cells
        for row in range(self.grid.rows):
            pygame.draw.line(self.screen, (0, 180, 240), (0, row * CELL), (self.grid.width(), row * CELL))

        for col in range(self.grid.cols):
            pygame.draw.line(self.screen, (0, 180, 240), (col * CELL, 0), (col * CELL, self.grid.height()))

        # Draw objects
        for pos, obj in self.grid:

            if obj == WALL:
                self.screen.blit(WALL_TILE, self.grid.rect(pos))
            elif obj == DIAMOND:
                self.screen.blit(DIAMOND_TILE, self.grid.rect(pos))
            elif obj == LOCK:
                self.screen.blit(LOCK_TILE, self.grid.rect(pos))
            elif obj == GREEN_LOCK:
                self.screen.blit(GREEN_LOCK_TILE, self.grid.rect(pos))
            elif obj == FRIEND:
                self.screen.blit(FRIEND_TILE, self.grid.rect(pos))
            elif obj == ARROW_DOWN:
                self.screen.blit(ARROW_DOWN_TILE, self.grid.rect(pos))
            elif obj == ARROW_UP:
                self.screen.blit(ARROW_UP_TILE, self.grid.rect(pos))
            elif obj == ARROW_LEFT:
                self.screen.blit(ARROW_LEFT_TILE, self.grid.rect(pos))
            elif obj == ARROW_RIGHT:
                self.screen.blit(ARROW_RIGHT_TILE, self.grid.rect(pos))
            elif obj == KEY:
                self.screen.blit(KEY_TILE, self.grid.rect(pos))
            elif obj == DOOR:
                self.screen.blit(DOOR_TILE, self.grid.rect(pos))
            elif obj == SLIME:
                self.screen.blit(SLIME_TILE, self.grid.rect(pos))


        # Draw the message board
        if self.messageRect is not None:
            pygame.draw.rect(self.screen, (0, 161, 228), self.messageRect)
            labels = []
            x = self.messageRect[0]
            y = self.messageRect[1]

            if isinstance(self.message, list):
                lines = self.message
            else:
                lines = self.message.splitlines()

            for line in lines:
                label = self.font.render(line, 1, (0, 0, 0))
                self.screen.blit(label, (x, y))
                y += 35

        # Draw the player
        x = player_x or self.grid.xy(self.col, self.row)[0]
        y = player_y or self.grid.xy(self.col, self.row)[1]
        if self.won:
            self.screen.blit(PLAYER_WON_TILE, (x, y, CELL, CELL))
        else:
            if self.red:
                self.screen.blit(PLAYER_TILE_RED, (x, y, CELL, CELL))
            else:
                if self.sliding:
                    self.screen.blit(PLAYER_TILE_SLIDING, (x, y, CELL, CELL))
                else:
                    self.screen.blit(PLAYER_TILE, (x, y, CELL, CELL))

        # update the display
        pygame.display.update()

        # Sleep for one frame
        self.clock.tick(60)

    def get_lock_in_front(self):
        for lock in self.locks:
            if lock.position is not None:
                if lock.position == [self.col + 1, self.row]:
                    return lock
            else:
                return lock
        raise Exception("No lock found")

    def look(self):
        obj = self.grid.object_in_sight()
        result = None
        if obj == LOCK:
            result = 'orange lock'
        elif obj == GREEN_LOCK:
            result = 'green lock'

        if result is None:
            self.message = "There is nothing in sight"
        else:
            self.message = [
                f"In front of you you see {result}.",
                f"(the look() function returns '{result}')"
            ]

        self._redraw()
        return result

    def move(self, col_step, row_step):
        newcol = self.col + col_step
        newrow = self.row + row_step

        # Check for collision
        if self.grid[newcol, newrow] in (WALL, LOCK, GREEN_LOCK, FRIEND, DOOR):
            # Animate that can't move
            self.red = True
            for x in range(6):  # 6 frames, 1/10 sec
                self._redraw()
            self.red = False
            self._redraw()

            return

        # Animate movement
        oldx, oldy = self.grid.xy(self.col, self.row)
        self.col = newcol
        self.row = newrow
        x, y = self.grid.xy(self.col, self.row)
        frames = 15
        dx = (x - oldx) / frames
        dy = (y - oldy) / frames

        for i in range(frames + 1):
            self._redraw(oldx + dx * i, oldy + dy * i)

        # Insert a small pause between steps
        self._redraw()

        # Check if we are on an arrow
        if self.grid[self.col, self.row] in (ARROW_LEFT, ARROW_RIGHT, ARROW_UP, ARROW_DOWN):
            if self.grid[self.col, self.row] == ARROW_LEFT:
                direction = (-1, 0)
            elif self.grid[self.col, self.row] == ARROW_RIGHT:
                direction = (1, 0)
            elif self.grid[self.col, self.row] == ARROW_UP:
                direction = (0, -1)
            else:
                direction = (0, 1)
            self.sliding = True
            self.move(*direction)
            self.sliding = False
            self._redraw()
            return

        # Check if we ended up in front of a lock
        if self.grid[self.col + 1, self.row] == LOCK:
            # Show what the lock says
            self.message = self.get_lock_in_front().message_in_front
            self._redraw()

        # Check if we ended up in front of a friend
        if self.grid[self.col + 1, self.row] == FRIEND:
            self.message = self.friends[0].message_in_front
            self._redraw()

        # Check if we have stepped on a key
        if self.grid[self.col, self.row] == KEY:
            self.message = "You collected a key!"
            self.keys += 1
            del self.grid[self.col, self.row]
            self._redraw()

        # Check if we have reached the diamond
        if self.grid[self.col, self.row] == DIAMOND:
            self.message = "Congratulations! You won!!!"
            del self.grid[self.col, self.row]  # removing the diamond
            self.won = True
            self._redraw()

    def open_lock(self, *codes):

        self.message = f"You are trying to open the lock with code: {', '.join([str(x) for x in codes])}."

        self._redraw()
        sleep(1)
        # Check if we are in front of a lock
        if self.grid[self.col + 1, self.row] not in (LOCK, GREEN_LOCK):
            self.message = "There is no lock in front of you"
            self._redraw()
            return False

        # Check if the codes are correct
        lock = self.get_lock_in_front()
        if not lock.open(*codes):
            self.message = lock.message_wrong_code
            if lock.auto_destroys:
                self.grid[self.col+1, self.row] = 'X'
                self.locks.remove(lock)
            self._redraw()
            sleep(1)
            return False

        # If the code is correct
        self.message = lock.message_when_open
        del self.grid[self.col + 1, self.row]
        self.locks.remove(lock)
        self._redraw()
        sleep(1)
        return True

    def open_door(self):
        door = self.grid[self.col+1, self.row]
        if door != DOOR:
            self.message = "There is no door to open"
            self._redraw()
            return

        door = self.doors.pop(0)

        if self.keys >= door['keysRequired']:
            self.message = "You opened the door!"
            del self.grid[self.col+1, self.row]
            self._redraw()
            return

        self.message = [
            "You do not have enough keys to open the door.",
            f"This door requries {door['keysRequired']} keys.",
            f"You have collected {self.keys} keys."
        ]
        self._redraw()

    def ask(self):
        sleep(.5)
        # Check if we are in front of a friend
        if self.grid[self.col + 1, self.row] != FRIEND:
            self.message = "There is no one to ask in front of you."
            self._redraw()
            return

        friend = self.friends[0]
        self.message = friend.message
        self._redraw()
        sleep(1)
        self.friends.pop(0)
        del self.grid[self.col + 1, self.row]
        self._redraw()
        sleep(1)
        return friend.data

    def run(self):
        while self.running:
            # Did the user click the window close button?
            for event in pygame.event.get():
                if self.keyboard and event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move(0, 1)
                    elif event.key == pygame.K_UP:
                        self.move(0, -1)

                if event.type == pygame.QUIT:
                    self.running = False

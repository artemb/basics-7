import json

from games._lib.grid_game import CodingGame

game = None


def create_game(mapfile=None):
    global game

    if mapfile is None:
        mapfile = "map"

    if isinstance(mapfile, dict):
        mapdata = mapfile
    else:
        with open(str(mapfile) + ".json", 'r') as f:
            mapdata = json.load(f)

    game = CodingGame(mapdata)


def right(steps=1):
    for x in range(steps):
        game.move(1, 0)


def left(steps=1):
    for x in range(steps):
        game.move(-1, 0)


def down(steps=1):
    for x in range(steps):
        game.move(0, 1)


def up(steps=1):
    for x in range(steps):
        game.move(0, -1)


def open_lock(*codes):
    return game.open_lock(*codes)

def ask(question=""):
    # Ignore question
    return game.ask()

def look():
    return game.look()


def run():
    game.run()

def open_door():
    return game.open_door()
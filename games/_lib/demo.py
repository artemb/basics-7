from games._lib.gamelib import *

conf = {
    "map": [
        "XXXXXXXXXXXXX",
        "X X FGGGGG  X",
        "X X XXXXXX  X",
        "XP  X   FX VX",
        "X X X XXXX  X",
        "X X>> L S   X",
        "XXXXXXXXXXXXX"
    ],
    "title": "Demo",
    "allowKeyboard": True,
    "welcomeMessage": "Hello"
}

create_game(conf)

run()
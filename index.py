# Run Away
# By James Nicholls, Kelsey Kloosterman, Lukas Adie, and Sharaf Syed
# Made for SE 2250, made for life

import pygame as pyg


# This method starts the game.
def init():
    pyg.init()

    # Separate Surfaces allows for the game to run at any (16:9) resolution at fullscreen and scale properly.
    sys_screen = pyg.display.set_mode((0,0), pyg.FULLSCREEN)
    game_screen = pyg.Surface((256,144))

    # Initialize level

if __name__ == "__main__":
    init()
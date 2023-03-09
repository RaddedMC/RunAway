# Run Away
# By James Nicholls, Kelsey Kloosterman, Lukas Adie, and Sharaf Syed
# Made for SE 2250, made for life

# Imports
import pygame as pyg
from core_classes.world.block import block
from constants_config import TILE_SIZE

class level:
    # This default size will give us a 16x9 grid of blocks to work with
    # The default platform_grid is just a floor
    def __init__(self, size = (256//16,144//16), background_img = None, platform_grid = None):

        if platform_grid == None:
            # Use a default platform grid that has just a basic floor if none is specified
            default_block = "res/tile/cake_test.png"
            platform_grid = []
            for i in range(0, size[1]-1):
                platform_grid.append(False)
            platform_grid.append(default_block)
            platform_grid = [platform_grid for i in range(0,size[0])]

        # Create sprite group
        self.blocks = pyg.sprite.Group()
        for x in range(0, len(platform_grid)):
            for y in range(0, len(platform_grid[x])):
                if not platform_grid[x][y] == False:
                    self.blocks.add(block(image = platform_grid[x][y], xpos = x*TILE_SIZE, ypos= y*TILE_SIZE))
# Run Away
# By James Nicholls, Kelsey Kloosterman, Lukas Adie, and Sharaf Syed
# Made for SE 2250, made for life
import pygame as pyg
from constants_config import TILE_SIZE

class block(pyg.sprite.Sprite):
    def __init__(self, image, xpos, ypos):

        pyg.sprite.Sprite.__init__(self)
        
        self.image = pyg.image.load(image)
        self.image = pyg.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = pyg.Rect(xpos, ypos, TILE_SIZE, TILE_SIZE)
# Run Away
# By James Nicholls, Kelsey Kloosterman, Lukas Adie, and Sharaf Syed
# Made for SE 2250, made for life
import pygame as pyg

class block(pyg.sprite.Sprite):
    def __init__(self, image, xpos, ypos):
        tile_size = 16

        pyg.sprite.Sprite.__init__(self)
        
        self.image = pyg.image.load(image)
        # self.image = pyg.transform.scale(self.image, (tile_size, tile_size))
        self.rect = pyg.Rect(xpos, ypos, 16, 16)
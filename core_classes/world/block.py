# Run Away
# By James Nicholls, Kelsey Kloosterman, Lukas Adie, and Sharaf Syed
# Made for SE 2250, made for life
import pygame as pyg
from core_classes.spawnable import spawnable

class block(spawnable):
    def __init__(self, image, xpos, ypos):
        spawnable.__init__(self, {"x":xpos, "y":ypos}, image)
        pyg.sprite.Sprite.__init__(self)
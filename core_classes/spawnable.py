# Run Away
# By James Nicholls, Kelsey Kloosterman, Lukas Adie, and Sharaf Syed
# Made for SE 2250, made for life

# Imports
import pygame as pyg
from constants_config import TILE_SIZE

# Used for players, enemies, NPCs, and other in game entities that can move
class spawnable(pyg.sprite.Sprite):
    def __init__(self, spawn_position, sprite, size = {"x": 1, "y": 1}):

        sprite_res = {"x": TILE_SIZE*size["x"], "y": TILE_SIZE*size["y"]}

        pyg.sprite.Sprite.__init__(self)

        self.image = pyg.image.load(sprite)
        self.image = pyg.transform.scale(self.image, (sprite_res["x"], sprite_res["y"]))
        self.rect = pyg.Rect(spawn_position["x"], spawn_position["y"], sprite_res["x"], sprite_res["y"])
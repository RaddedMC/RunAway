# Run Away
# By James Nicholls, Kelsey Kloosterman, Lukas Adie, and Sharaf Syed
# Made for SE 2250, made for life

# Imports
import pygame as pyg
from constants_config import TILE_SIZE
from core_classes.spawnable import spawnable

# Used for any Spawnable that can move!
class moving_entity(spawnable):
    def __init__(self, spawn_position, sprite, size = {"x": 1, "y": 1}):
        spawnable.__init__(self, spawn_position, )
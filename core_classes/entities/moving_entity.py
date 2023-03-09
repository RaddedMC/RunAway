# Run Away
# By James Nicholls, Kelsey Kloosterman, Lukas Adie, and Sharaf Syed
# Made for SE 2250, made for life

# Imports
import pygame as pyg
from constants_config import TILE_SIZE
from core_classes.spawnable import spawnable

# Used for any Spawnable that can move!
class moving_entity(spawnable):
    def __init__(self, spawn_position, sprite="res/tile/circle_player_test.png", size = {"x": 1, "y": 2}, gravity = 0):
        spawnable.__init__(self, spawn_position, sprite, size)

        self.speed = {"x": 0, "y": 0}
        self.gravity = gravity

    def set_speed(self, x,y):
        self.speed = {"x": x, "y": y}

    def update_position(self, time_scale = 0):
        # Move the rectangle
        self.rect.move(self.speed["x"]*time_scale, self.speed["y"]*time_scale)

        # Decrease y by gravity
        self.speed["y"] -= self.gravity * time_scale
# Run Away
# By James Nicholls, Kelsey Kloosterman, Lukas Adie, and Sharaf Syed
# Made for SE 2250, made for life

# Imports
import pygame as pyg

# Used for players, enemies, NPCs, and other in game entities that can move
class spawnable:
    def __init__(spawn_position, sprite, speed = {x: 0, y: 0}):
        
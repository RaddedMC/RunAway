import pygame

from entity import AnimatedEntity

class Player(AnimatedEntity):
    def __init__(self, pos, image, speed, groups):
        super().__init__(groups)
        pass
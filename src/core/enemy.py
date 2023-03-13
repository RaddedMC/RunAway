import pygame

from entity import AnimatedEntity

class Enemy(AnimatedEntity):
    # Better to take in an image + coords or just a rectangle only?
    def __init__(self, pos, image, speed, groups):
        super().__init__(groups)
        self.speed = speed
        pass
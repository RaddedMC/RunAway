import pygame

from core.entity import AnimatedEntity


class Enemy(AnimatedEntity):
    def __init__(self, pos, image, speed, groups):
        super().__init__(groups)
        self.speed = speed
        pass

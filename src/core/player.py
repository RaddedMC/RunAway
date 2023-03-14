from pathlib import Path

import pygame

from core.entity import AnimatedEntity
from utils import tools


class Player(AnimatedEntity):
    def __init__(self, groups: pygame.sprite.Group, pos: tuple, root_dir: str):
        super().__init__(groups, pos, root_dir)

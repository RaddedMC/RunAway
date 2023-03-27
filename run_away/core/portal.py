import pygame
from core.entity import InteractableEntity

import config
from config import BASE_PATH

class Portal(InteractableEntity):
    def __init__(
            self,
            groups: pygame.sprite.Group,
            collidable_sprites: pygame.sprite.Group,
            pos: tuple,
            colour: str,
            level_path: str
            
    ):
        self.config = config.PORTAL_DATA
        root_dir = f"{BASE_PATH}/gfx/objects/portal/{colour}"
        super().__init__(groups, collidable_sprites, pos, root_dir)
        self.level_path = level_path
        self.animation_speed = self.config["animation_speed"]
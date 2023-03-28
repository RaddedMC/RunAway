import pygame
from core.NPC import NPC

import config
from config import BASE_PATH

class Portal(NPC):
    def __init__(
            self,
            groups: pygame.sprite.Group,
            collidable_sprites: pygame.sprite.Group,
            pos: tuple,
            colour: str,
            level_path: str,
            dialogue  = ["Press Z to Travel"]           
    ):
        self.config = config.PORTAL_DATA
        root_dir = f"{BASE_PATH}/gfx/objects/portal/{colour}"
        super().__init__(groups, collidable_sprites, pos, root_dir, dialogue, speed=0, gravity=0)
        self.level_path = level_path
        self.animation_speed = self.config["animation_speed"]
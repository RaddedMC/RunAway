import config
import pygame
from config import BASE_PATH
from core.level import LevelType
from core.NPC import NPC


class Portal(NPC):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple,
        colour: str,
        target_level: LevelType,
        dialogue=["Press Z to Travel"],
    ):
        self.config = config.PORTAL_DATA
        root_dir = (
            f"{BASE_PATH}/gfx/objects/portal/{colour}"  # TODO: should we enforce pathlib.Path everywhere or allow both Path and str to be passed in?
        )
        super().__init__(
            groups, collidable_sprites, pos, root_dir, dialogue, speed=0, gravity=0
        )
        self.target_level = target_level
        self.animation_speed = self.config["animation_speed"]

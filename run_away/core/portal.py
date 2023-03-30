import os
from pathlib import Path
from typing import Union

import pygame
from core.level import LevelType
from core.npc import NPC


class Portal(NPC):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple[int, int],
        root_dir: Union[str, Path],
        animation_speed: int,
        dialogue: list[str],
        colour: str,
        target_level: LevelType,
    ) -> None:
        if type(root_dir) is Path:
            root_dir = root_dir.joinpath(colour)
        else:
            root_dir = os.path.join(root_dir, colour)

        super().__init__(
            groups,
            collidable_sprites,
            pos,
            root_dir,
            animation_speed,
            dialogue,
        )
        self.target_level = target_level

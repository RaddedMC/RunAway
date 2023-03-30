import random
from pathlib import Path
from typing import Union

import config
import pygame
from core.entity import InteractableEntity
from utils.tools import get_sounds_by_key


class NPC(InteractableEntity):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple[int, int],
        root_dir: Union[str, Path],
        animation_speed: int,
        dialogue: list[str],
    ) -> None:
        super().__init__(
            groups, collidable_sprites, pos, root_dir, animation_speed, 0, 0
        )
        self.dialogue = dialogue
        self.msg_index = 0
        self.message = config.GAME_FONT.render(
            f"{self.dialogue[self.msg_index]}", True, (255, 255, 255)
        )
        self.message_rect = self.message.get_rect(topleft=pos)

    def interact(self) -> None:
        self.message = config.GAME_FONT.render(
            f"{self.dialogue[self.msg_index]}", True, (255, 255, 255)
        )
        display_surface = pygame.display.get_surface()
        display_surface.blit(self.message, self.message_rect)
        self.msg_index += 1
        self.msg_index = self.msg_index % len(self.dialogue)

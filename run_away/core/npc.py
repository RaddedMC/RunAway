from pathlib import Path
from typing import Union

import pygame

from run_away import config
from run_away.core.entity import InteractableEntity


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
        display_rect = pygame.display.get_surface().get_rect()
        self.message_rect = self.message.get_rect(midtop=(display_rect.centerx, 100))

    def interact(self):
        self.message = config.GAME_FONT.render(
            f"{self.dialogue[self.msg_index]}", True, (255, 255, 255)
        )
        display_surface = pygame.display.get_surface()
        display_surface.blit(self.message, self.message_rect)
        self.msg_index += 1
        self.msg_index = self.msg_index % len(self.dialogue)

from pathlib import Path

import pygame

from run_away import config
from run_away.core.entity import AnimatedEntity


class Weapon(AnimatedEntity):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple,
        root_dir: Path,
        damage: int,
        direction: str,
        player,
    ):
        super().__init__(groups, collidable_sprites, pos, root_dir)
        self.damage = damage
        self.rect.move_ip(config.WEAPON_DATA["offset"][direction])
        self.hitbox = self.create_hitbox()
        self.player = player
        self.update_direction()

    def get_damage(self) -> int:
        return self.damage

    def update_direction(self) -> None:
        direction = self.player.get_direction_str()
        if direction == "left":
            self.direction.x = -1
            self.flip_sprite = True
        elif direction == "right":
            self.direction.x = 1
            self.flip_sprite = False

    def update_position(self) -> None:
        self.rect = self.image.get_rect(topleft=self.player.rect.topleft).move(
            config.WEAPON_DATA["offset"][self.player.get_direction_str()]
        )
        self.hitbox = self.create_hitbox()

    def create_hitbox(self) -> pygame.Rect:
        return self.rect.copy().inflate(
            tuple(
                l * r
                for l, r in zip(  # noqa: E741
                    self.rect.size, config.WEAPON_DATA["scale"]
                )
            )
        )

    def update(self, dt) -> None:
        self.update_direction()
        self.update_position()
        super().update(dt)

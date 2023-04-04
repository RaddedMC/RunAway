import config
import pygame
from core.entity import Entity


class Weapon(Entity):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple,
        image: pygame.Surface,
        damage: int,
        direction: str,
        player,
    ):
        super().__init__(groups, collidable_sprites, pos, image)
        self.damage = damage
        self.rect.move_ip(config.WEAPON_DATA["offset"][direction])
        self.hitbox = self.create_hitbox()
        self.player = player

        if direction == "left":
            self.direction.x = -1
            self.flip_sprite = True
        elif direction == "right":
            self.direction.x = 1
            self.flip_sprite = False

    def get_damage(self) -> int:
        return self.damage

    def update_position(self) -> None:
        self.rect = self.image.get_rect(topleft=self.player.rect.topleft).move(
            config.WEAPON_DATA["offset"][self.player.get_direction_str()]
        )
        self.hitbox = self.create_hitbox()

    def create_hitbox(self) -> pygame.Rect:
        return self.rect.copy().inflate(
            tuple(l * r for l, r in zip(self.rect.size, config.WEAPON_DATA["scale"]))
        )

    def update(self, dt) -> None:
        super().update(dt)
        self.update_position()

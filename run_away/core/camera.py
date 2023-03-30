import config
import pygame
from core.player import Player


class CameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, surface: pygame.Surface, player: Player) -> None:
        self.offset.x = player.rect.centerx - surface.get_width() / 2
        self.offset.y = player.rect.centery - surface.get_height() / 2

        for sprite in self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            surface.blit(sprite.image, offset_rect)

            if config.DEBUG_SHOW_HITBOXES is True:
                hitbox = sprite.hitbox.copy()
                hitbox.center -= self.offset
                pygame.draw.rect(surface, (255, 0, 0), hitbox, 1)

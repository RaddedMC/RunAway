import pygame

from core.player import Player


class CameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player: Player):
        self.offset.x = player.rect.centerx - self.screen.get_width() / 2
        self.offset.y = player.rect.centery - self.screen.get_height() / 2

        # FIXME: sorting not necessary because our game is a platformer
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

        # for layer in LAYERS.values():
        #     for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
        #         if sprite.z == layer:
        #             offset_rect = sprite.rect.copy()
        #             offset_rect.center -= self.offset
        #             self.display_surface.blit(sprite.image, offset_rect)

import pygame

from player import Player

class CameraGroup(pygame.sprite.Group):
    def __init__(self, sprites) -> None:
        super().__init__(sprites)
        self.screen = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player: Player):
        self.offset.x = player.rect.centerx - self.screen.get_width() / 2
        self.offset.y = player.rect.centery - self.screen.get_height() / 2

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.screen.blit(sprite.image, offset_rect)

        # for layer in LAYERS.values():
        #     for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
        #         if sprite.z == layer:
        #             offset_rect = sprite.rect.copy()
        #             offset_rect.center -= self.offset
        #             self.display_surface.blit(sprite.image, offset_rect)
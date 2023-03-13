import pygame as pg
import sys
from pytmx.util_pygame import load_pygame
from pathlib import Path

class Entity(pg.sprite.Sprite):
    def __init__(self, pos, surf: pg.Surface, groups) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class Player(Entity):
    def __init__(self, pos, surf: pg.Surface, groups) -> None:
        super().__init__(pos, surf, groups)

class CameraGroup(pg.sprite.Group):
    def __init__(self, sprites) -> None:
        super().__init__(sprites)
        self.screen = pg.display.get_surface()
        self.offset = pg.math.Vector2()

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



TILE_SIZE = 16

pg.init()
screen = pg.display.set_mode((640, 360))
tmx_data = load_pygame(Path("./resources/levels/level_spring.tmx").resolve())
# print(dir(tmx_data))
# print(tmx_data.layers)
collision_sprites = pg.sprite.Group()
all_sprites = CameraGroup()

for layer in tmx_data.visible_layers:
    # Only get tile layers
    if hasattr(layer, "data"):
        for x,y,surf in layer.tiles():
            Entity((x*TILE_SIZE, y*TILE_SIZE), surf, all_sprites)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    screen.fill("black")
    all_sprites.draw(screen)
    pg.display.update()
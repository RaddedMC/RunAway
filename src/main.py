import core.entity
import pygame
import sys

from core.camera import CameraGroup
from core.enemy import Enemy
from core.player import Player

from pytmx.util_pygame import load_pygame
from pathlib import Path


TILE_SIZE = 16

pygame.init()
screen = pygame.display.set_mode((640, 360))
tmx_data = load_pygame(Path("./resources/levels/level_spring.tmx").resolve())
# print(dir(tmx_data))
# print(tmx_data.layers)
collision_sprites = pygame.sprite.Group()
all_sprites = CameraGroup()

for layer in tmx_data.visible_layers:
    # Only get tile layers
    if hasattr(layer, "data"):
        for x,y,surf in layer.tiles():
            Entity((x*TILE_SIZE, y*TILE_SIZE), surf, all_sprites)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("black")
    all_sprites.draw(screen)
    pygame.display.update()
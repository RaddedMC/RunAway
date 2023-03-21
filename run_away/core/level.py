from pathlib import Path

import config
import pygame
from core.camera import CameraGroup
from core.entity import Entity
from core.player import Player
from core.enemy import Grunt
from pytmx.util_pygame import load_pygame
from utils.tools import debug


class Level:
    def __init__(self, level_path) -> None:
        """
        To solve the issue of resolution scaling, this game draws all of its sprites to a
        small (256px by 144px) surface, then upscales this surface to the resolution of the
        user's display before finally updating the display.

        This makes designing sprites, levels, etc. much easier as we're enforcing a single
        aspect ratio with the added benefit being that our game will also look the same to all
        players.
        """
        self.render_surface = pygame.Surface(config.RENDER_AREA)
        self.display_surface = pygame.display.get_surface()
        # print(self.display_surface.get_size())

        self.all_sprites = CameraGroup()
        self.collidable_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.import_assets(level_path)

    def resize_render_surface(self):
        self.render_surface = pygame.Surface(config.RENDER_AREA)

    def import_assets(self, level_path):
        tmx_data = load_pygame(
            Path(level_path).resolve()
        )
        # print(dir(tmx_data))
        # print(tmx_data.layers)

        for layer in tmx_data.visible_layers:
            # Only get tile layers
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    Entity(
                        [self.all_sprites, self.collidable_sprites],
                        self.collidable_sprites,
                        (x * config.TILE_SIZE, y * config.TILE_SIZE),
                        surf,
                    )

            # print(dir(layer))  # DEBUG

        for obj in tmx_data.get_layer_by_name("Player"):
            if obj.name == "Start":
                # TODO: should Player belong to collidable_sprites?
                Player(
                    [self.all_sprites, self.player],
                    self.collidable_sprites,
                    (obj.x, obj.y),
                    "./run_away/resources/gfx/player/",
                    speed=90,
                    gravity=200,  # 100, make world property?
                    jump_speed=150  # 120
                )
        
        try:
            for obj in tmx_data.get_layer_by_name("Enemies"):
                if obj.type == "Grunt":
                    Grunt(
                        [self.all_sprites, self.enemies, self.collidable_sprites],
                        self.collidable_sprites,
                        (obj.x, obj.y),
                        "./run_away/resources/gfx/enemies/grunt/",
                        speed=40,
                        gravity=100, # FIXME: hardcoded for now, make world property?
                        colour="yellow"
                    )
        except ValueError:
            # This level probably has no enemies
            pass
        

    def run(self, dt):
        # self.display_surface.fill("black")
        # self.all_sprites.draw(display_surface)
        # pygame.display.flip()

        # Draw sprites, upscale the render surface and display to the user's screen
        self.render_surface.fill("black")
        self.all_sprites.update(dt)
        self.all_sprites.custom_draw(self.render_surface, self.player.sprite)
        scaled_display = pygame.transform.scale(
            self.render_surface,
            (self.display_surface.get_width(), self.display_surface.get_height()),
        )
        self.display_surface.blit(scaled_display, (0, 0))
        if config.DEBUG_UI:
            debug(self.player.sprite.status)
            debug(f"Direction: {self.player.sprite.direction}", 40)
            debug(f"Speed: {self.player.sprite.speed}", 60)
            debug(f"Colliding: {pygame.sprite.spritecollide(self.player.sprite, self.collidable_sprites, False)}", 80)
            debug(f"On Ground: {self.player.sprite.on_ground}", 100)
            debug(f"Buffer: {self.player.sprite.pixels_buffer}", 120)
        pygame.display.flip()

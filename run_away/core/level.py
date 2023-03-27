from pathlib import Path

import config
import pygame
from core.camera import CameraGroup
from core.entity import Entity, Hazard
from core.player import Player
from core.enemy import Grunt
from core.portal import Portal
from pytmx.util_pygame import load_pygame
from utils.tools import debug
import os
import random


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
        self.lvl_path = level_path
        self.render_surface = pygame.Surface(config.RENDER_AREA)
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()
        self.collidable_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.import_assets(level_path)

    def resize_render_surface(self):
        self.render_surface = pygame.Surface(config.RENDER_AREA)

    # Load level items
    def import_assets(self, level_path):
        tmx_data = load_pygame(Path(level_path).resolve())

        # Load blocks
        for layer in tmx_data.visible_layers:
            # Only get tile layers
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    if layer.name == "Ground":
                        Entity(
                            [self.all_sprites, self.collidable_sprites],
                            self.collidable_sprites,
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
                        )
                    elif layer.name == "Bottom Spikes":
                        Hazard(
                            [self.all_sprites, self.collidable_sprites],
                            self.collidable_sprites,
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
                            type="bottom",
                        )
                    elif layer.name == "Top Spikes":
                        Hazard(
                            [self.all_sprites, self.collidable_sprites],
                            self.collidable_sprites,
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
                            type="top",
                        )
                    elif layer.name == "Left Spikes":
                        Hazard(
                            [self.all_sprites, self.collidable_sprites],
                            self.collidable_sprites,
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
                            type="left",
                        )
                    elif layer.name == "Right Spikes":
                        Hazard(
                            [self.all_sprites, self.collidable_sprites],
                            self.collidable_sprites,
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
                            type="right",
                        )
                    elif layer.name == "vLayer1":
                        Entity(
                            [self.all_sprites],
                            None,
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
                        )
                    elif layer.name == "vLayer2":
                        Entity(
                            [self.all_sprites],
                            None,
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
                        )

        # Spawn player
        for obj in tmx_data.get_layer_by_name("Player"):
            if obj.name == "Start":
                # TODO: should Player belong to collidable_sprites?
                Player(
                    [self.all_sprites, self.player],
                    [self.collidable_sprites, self.enemies],
                    (obj.x, obj.y),
                    "./run_away/resources/gfx/player/",
                    speed=120,
                    gravity=275,
                    jump_speed=175,
                )

        # Select grunt colour
        grunt_colour = "green"
        if "lightning" in level_path:
            grunt_colour = "yellow"
        elif "snow" in level_path:
            grunt_colour = "blue"
        elif "rain" in level_path:
            grunt_colour = "red"

        # Spawn grunts, if any exist
        try:
            for obj in tmx_data.get_layer_by_name("Enemies"):
                if obj.type == "Grunt":
                    Grunt(
                        [self.all_sprites, self.enemies],
                        [self.collidable_sprites, self.player],
                        (obj.x, obj.y),
                        speed=40,
                        gravity=100,  # FIXME: hardcoded for now, make world property?
                        colour=grunt_colour,
                    )
        except ValueError:
            # This level probably has no enemies
            pass

        try:
            for obj in tmx_data.get_layer_by_name("Interactables"):
                # Load portals
                if obj.type == "Portal":
                    Portal(
                        [self.all_sprites, self.portals],
                        None,
                        (obj.x, obj.y),
                        colour="blue",
                        level_path="run_away/resources/levels/level_"
                        + obj.name[0 : obj.name.find("_")].lower()
                        + ".tmx",
                    )
        except ValueError:
            pass

    def check_portals(self):
        collided = pygame.sprite.groupcollide(self.player, self.portals, False, False)
        if self.player.sprite in collided:
            return collided[self.player.sprite][0]
        else:
            return False

    def run(self, dt):
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
            debug(
                f"Colliding: {pygame.sprite.spritecollide(self.player.sprite, self.collidable_sprites, False)}",
                80,
            )
            debug(f"On Ground: {self.player.sprite.on_ground}", 100)
            debug(f"Buffer: {self.player.sprite.pixels_buffer}", 120)
            debug(
                f"Position: ({self.player.sprite.rect.x}, {self.player.sprite.rect.y})",
                140,
            )
            debug(f"Player Health: {self.player.sprite.health}", 160)
            debug(f"On Spikes: {self.player.sprite.on_hazard}", 180)

        pygame.display.flip()
        return self.check_portals()

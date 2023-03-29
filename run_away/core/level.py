import os
import random
from enum import Enum
from pathlib import Path

import config
import pygame
from config import LEVELS_PATH
from core.camera import CameraGroup
from core.enemy import Grunt
from core.entity import AnimatedEntity, Entity, Hazard
from core.player import Player
from pytmx.util_pygame import load_pygame
from utils.tools import debug


class LevelType(Enum):
    RAIN = LEVELS_PATH.joinpath("level_rain.tmx").resolve()
    WIND = LEVELS_PATH.joinpath("level_wind.tmx").resolve()
    LIGHTNING = LEVELS_PATH.joinpath("level_lightning.tmx").resolve()
    SNOW = LEVELS_PATH.joinpath("level_snow.tmx").resolve()
    HUB = LEVELS_PATH.joinpath("level_hub.tmx").resolve()
    HUB_RAIN_ACCESS = LEVELS_PATH.joinpath("level_hub_rainaccess.tmx").resolve()
    RAIN_RETURN = LEVELS_PATH.joinpath("level_rainreturn.tmx").resolve()

    @classmethod
    def list(cls):
        return list(map(lambda e: e.value, cls))


from core.portal import Portal


class Level:
    def __init__(self, kind: LevelType, stats) -> None:
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

        self.all_sprites = CameraGroup()
        self.collidable_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.coins = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()

        self.stats = stats
        # TODO create dictionary with all player possessions and attributes to pass down?
        # self.items = {coins :0, }

        self.kind = kind
        self.path: Path = self.kind.value

        self.import_assets()

    def resize_render_surface(self):
        self.render_surface = pygame.Surface(config.RENDER_AREA)

    # Load level items
    def import_assets(self):
        tmx_data = load_pygame(self.path.resolve())

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
                # TODO: add Player stats attribute that contains coins?
                Player(
                    [self.all_sprites, self.player],
                    [self.collidable_sprites, self.enemies],
                    (obj.x, obj.y),
                    "./run_away/resources/gfx/player/",
                    speed=120,
                    gravity=275,
                    jump_speed=175,
                    coins=self.stats["coins"],
                )

        # Select grunt colour
        grunt_colour = "green"
        if self.kind is LevelType.LIGHTNING:
            grunt_colour = "yellow"
        elif self.kind is LevelType.SNOW:
            grunt_colour = "blue"
        elif self.kind is LevelType.RAIN:
            grunt_colour = "red"

        # Spawn grunts, if any exist
        try:
            for obj in tmx_data.get_layer_by_name("Enemies"):
                if obj.type == "Grunt":
                    Grunt(
                        [self.all_sprites, self.enemies],
                        [self.collidable_sprites, self.player],
                        (obj.x, obj.y),
                        (
                            False,
                            False,
                            False,
                        ),  # FIXME: temporary, figure out way to determine this based on current level?
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
                        target_level=next(
                            (
                                level
                                for level in LevelType
                                if obj.name[0 : obj.name.find("_")].lower()
                                in str(level.value)
                            ),
                            None,  # TODO: this will need to be changed/removed once the final portal is implemented
                        ),
                    )
        except ValueError:
            pass

        try:
            for obj in tmx_data.get_layer_by_name("Consumables"):
                if obj.type == "Coin":
                    AnimatedEntity(
                        [self.all_sprites, self.coins],
                        [self.player],
                        (obj.x, obj.y),
                        "./run_away/resources/gfx/objects/coins",
                    )
        except ValueError:
            # level has no coins
            pass

    def check_portals(self):
        collided = pygame.sprite.groupcollide(self.player, self.portals, False, False)
        if self.player.sprite in collided:
            collided[self.player.sprite][0].interact()
            if self.player.sprite.status == "interacting":
                return collided[self.player.sprite][0]
        else:
            return False

    def check_coins(self):
        for coin in pygame.sprite.groupcollide(self.coins, self.player, True, False):
            # TODO add sfx
            self.player.sprite.get_coin()

    def check_interactables(self):
        if pygame.sprite.collide_rect(self.player.sprite, self.npcs):
            if self.player.sprite.status == "interacting":
                self.npcs.sprite.interact()

    def run(self, dt):
        # Draw sprites, upscale the render surface and display to the user's screen
        self.render_surface.fill("black")
        self.all_sprites.update(dt)
        self.all_sprites.custom_draw(self.render_surface, self.player.sprite)
        scaled_display = pygame.transform.scale(
            self.render_surface,
            (self.display_surface.get_width(), self.display_surface.get_height()),
        )
        self.check_coins()
        # TODO update entire stats dictionary at once?
        self.stats["coins"] = self.player.sprite.coins
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
            debug(f"Player Coins: {self.player.sprite.coins}", 180)
            self.check_portals()

        pygame.display.flip()
        return self.check_portals()

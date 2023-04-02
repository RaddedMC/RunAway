from enum import Enum
from pathlib import Path

import config
import pygame
from config import LEVELS_PATH
from core.camera import CameraGroup
from core.enemy import Flying, Grunt
from core.entity import AnimatedEntity, Block, Hazard
from core.npc import NPC
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
    HOME = LEVELS_PATH.joinpath("level_home.tmx").resolve()

    @classmethod
    def list(cls):
        return list(map(lambda e: e.value, cls))


from core.background import Background

from core.portal import Portal

class Level:
    def __init__(self, kind: LevelType, stats: dict) -> None:
        """
        To solve the issue of resolution scaling, this game draws all of its sprites to
        a small (256px by 144px) surface, then upscales this surface to the resolution
        of the user's display before finally updating the display.

        This makes designing sprites, levels, etc. much easier as we're enforcing a
        single aspect ratio with the added benefit being that our game will also look
        the same to all players.
        """
        self.render_surface = pygame.Surface(config.RENDER_AREA)
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()
        self.collidable_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.home = pygame.sprite.GroupSingle()
        self.coins = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.grunt_tiles = pygame.sprite.Group()

        self.stats = stats
        # TODO: create dictionary with all player possessions and attributes to pass down?
        # self.items = {coins :0, }

        self.kind = kind
        self.path: Path = self.kind.value

        self.import_assets()

    def resize_render_surface(self) -> None:
        self.render_surface = pygame.Surface(config.RENDER_AREA)

    # Load level items
    def import_assets(self):
        tmx_data = load_pygame(str(Path(self.path).resolve()))
        self.backgrounds = []

        self.screen_width = config.RENDER_AREA[0]
        self.screen_height = config.RENDER_AREA[1]

        # Load blocks
        for layer in tmx_data.visible_layers:

            # Load backgrounds
            if "Background" in layer.name:
                parallax_x = 1
                if hasattr(layer, "parallaxx"):
                    parallax_x = float(layer.parallaxx)

                parallax_y = 1
                if hasattr(layer, "parallaxy"):
                    parallax_y = float(layer.parallaxy)

                if not hasattr(layer, "offsetx"):
                    set_x = 0
                else:
                    set_x = layer.offsetx

                if not hasattr(layer, "offsety"):
                    set_y = 0
                else:
                    set_y = layer.offsety

                self.backgrounds.append(Background(
                    path_from_tiled=layer.source,

                    parallax_x=parallax_x,
                    parallax_y=parallax_y,

                    world_width=self.screen_width,
                    world_height=self.screen_height,

                    bg_width=tmx_data.width,
                    bg_height=tmx_data.height,

                    image_offset_x=set_x,
                    image_offset_y=set_y
                ))


            # Only get tile layers
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    if layer.name == "Ground":
                        Block(
                            [self.all_sprites, self.collidable_sprites],
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
                        )
                    elif layer.name == "Bottom Spikes":
                        Hazard(
                            [self.all_sprites, self.collidable_sprites],
                            self.collidable_sprites,
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
                            kind="bottom",
                        )
                    elif layer.name == "Top Spikes":
                        Hazard(
                            [self.all_sprites, self.collidable_sprites],
                            self.collidable_sprites,
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
                            kind="top",
                        )
                    elif layer.name == "Left Spikes":
                        Hazard(
                            [self.all_sprites, self.collidable_sprites],
                            self.collidable_sprites,
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
                            kind="left",
                        )
                    elif layer.name == "Right Spikes":
                        Hazard(
                            [self.all_sprites, self.collidable_sprites],
                            self.collidable_sprites,
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
                            kind="right",
                        )
                    elif layer.name == "vLayer1":
                        Block(
                            [self.all_sprites],
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
                        )
                    elif layer.name == "vLayer2":
                        Block(
                            [self.all_sprites],
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
                        )
                    elif layer.name == "GruntTiles":
                        Block(
                            [self.all_sprites, self.grunt_tiles],
                            (
                                x * config.TILE_SIZE,
                                y * config.TILE_SIZE,
                                config.TILE_SIZE,
                                config.TILE_SIZE,
                            ),
                        )

        try:
            for obj in tmx_data.get_layer_by_name("Interactables"):
                # Load portals
                if obj.type == "Portal":
                    Portal(
                        [self.all_sprites, self.portals],
                        None,
                        (obj.x, obj.y),
                        config.GFX_PATH.joinpath("objects", "portal"),
                        config.PORTAL_DATA["animation_speed"],
                        config.PORTAL_DATA["dialogue"],
                        colour="blue",
                        target_level=next(
                            (
                                level
                                for level in LevelType
                                if obj.name[0 : obj.name.find("_")].lower()
                                in str(level.value)
                            ),
                        ),
                    )
                elif self.kind == LevelType.HOME:
                    print("is end scene!")
                    print(obj.name, ", ", obj.type)
                    if obj.type == "Home":
                        from core.home import Home

                        Home(
                            [self.all_sprites, self.home],
                            None,
                            (obj.x, obj.y),
                            config.GFX_PATH.joinpath("objects", "home"),
                        )

                # if obj.type == "NPC":
                #     NPC(
                #         [self.all_sprites, self.npcs],
                #         None,
                #         (obj.x, obj.y),
                #         "./run_away/resources/gfx/NPCs/" + obj.name[0:obj.name.find("_")].lower() + "NPC",
                #         dialogue = ["get dunked on lol"]
                #     )
        except ValueError:
            pass

        # Spawn player
        for obj in tmx_data.get_layer_by_name("Player"):
            if obj.name == "Start":
                # TODO: add Player stats attribute that contains coins?
                Player(
                    [self.all_sprites, self.player],
                    [self.collidable_sprites, self.enemies],
                    (obj.x, obj.y),
                    config.GFX_PATH.joinpath("player"),
                    config.PLAYER_DATA["animation_speed"],
                    speed=config.PLAYER_DATA["stats"]["speed"],
                    gravity=config.PLAYER_DATA["gravity"],
                    health=config.PLAYER_DATA["stats"]["health"],
                    damage=config.PLAYER_DATA["stats"]["damage"],
                    jump_speed=config.PLAYER_DATA["jump_speed"],
                )
            elif obj.name == "Start:ForceLeft":
                AnimatedEntity(
                    [self.all_sprites, self.player],
                    [self.collidable_sprites],
                    (obj.x, obj.y),
                    config.GFX_PATH.joinpath("player"),
                    animation_speed=18,
                    speed=60,
                    gravity=275,
                ).direction = pygame.Vector2(-1, 0)
                self.player.sprite.status = "run"

        # Select grunt colour
        if self.kind is LevelType.LIGHTNING:
            grunt_colour = "yellow"
        elif self.kind is LevelType.SNOW:
            grunt_colour = "blue"
        elif self.kind is LevelType.RAIN:
            grunt_colour = "red"
        else:
            grunt_colour = "green"

        # TODO: find way to determine level progress and multiply factor to the enemy's health, damage, etc.

        # Spawn enemies, if any exist
        try:
            for obj in tmx_data.get_layer_by_name("Enemies"):
                if obj.type == "Grunt":
                    Grunt(
                        [self.all_sprites, self.enemies],
                        [self.collidable_sprites, self.player, self.grunt_tiles],
                        (obj.x, obj.y),
                        config.GFX_PATH.joinpath("enemies", "grunt"),
                        config.ENEMY_DATA["grunt"]["animation_speed"],
                        speed=config.ENEMY_DATA["grunt"]["stats"]["speed"],
                        gravity=100,  # FIXME: hardcoded for now, make world property?
                        health=config.ENEMY_DATA["grunt"]["stats"]["health"],
                        damage=config.ENEMY_DATA["grunt"]["stats"]["damage"],
                        player=self.player.sprite,
                        colour=grunt_colour,
                    )
                elif obj.type == "Flying":
                    Flying(
                        [self.all_sprites, self.enemies],
                        [self.collidable_sprites, self.player],
                        (obj.x, obj.y),
                        config.GFX_PATH.joinpath("enemies", "flying"),
                        config.ENEMY_DATA["flying"]["animation_speed"],
                        speed=config.ENEMY_DATA["flying"]["stats"]["speed"],
                        health=config.ENEMY_DATA["flying"]["stats"]["health"],
                        damage=config.ENEMY_DATA["flying"]["stats"]["damage"],
                        player=self.player.sprite,
                    )
        except ValueError:
            # This level probably has no enemies
            pass

        try:
            for obj in tmx_data.get_layer_by_name("Consumables"):

                if obj.type == "Coin":
                    AnimatedEntity(
                        [self.all_sprites, self.coins],
                        [self.player],
                        (obj.x, obj.y),
                        config.GFX_PATH.joinpath("objects", "coins"),
                    )
        except ValueError:
            # level has no coins
            pass

    def check_portals(self) -> None:
        collided = pygame.sprite.groupcollide(self.player, self.portals, False, False)
        if self.player.sprite in collided:
            collided[self.player.sprite][0].interact()
            if self.player.sprite.status == "interacting":
                return collided[self.player.sprite][0]
        else:
            return False

    def check_coins(self) -> None:
        for coin in pygame.sprite.groupcollide(self.coins, self.player, True, False):
            # TODO: add sfx
            self.player.sprite.get_coin()

    def check_interactables(self) -> None:
        if pygame.sprite.collide_rect(self.player.sprite, self.npcs):
            if self.player.sprite.status == "interacting":
                self.npcs.sprite.interact()
        
    def run(self, dt: float):

        for background in self.backgrounds:
            offset_x = -self.player.sprite.rect.x
            offset_y = -self.player.sprite.rect.y
            background.draw(offset_x,offset_y,self.render_surface)

        # Draw sprites, upscale the render surface and display to the user's screen
        self.all_sprites.update(dt)
        self.all_sprites.custom_draw(self.render_surface, self.player.sprite)

        if self.kind == LevelType.HOME:
            self.update_end_cutscene(dt)

        scaled_display = pygame.transform.scale(
            self.render_surface,
            (self.display_surface.get_width(), self.display_surface.get_height()),
        )

        self.display_surface.blit(scaled_display, (0, 0))
        # TODO: update entire stats dictionary at once?
        try:
            self.stats["coins"] = self.player.sprite.coins
            self.check_coins()
        except:
            # Above won't work in the end cutscene
            pass

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
        self.check_portals()
        pygame.display.flip()
        return self.check_portals()

    def update_end_cutscene(self, dt: float) -> None:
        # Create timer if doesn't exist
        if not hasattr(self, "timer"):
            self.timer = dt
        else:
            # Update timer based on delta-time
            self.timer += dt

        # Set Tye's speed
        if self.player.sprite.speed.x < 0:
            # RUN AWAY
            self.player.sprite.speed.x -= dt * 20
        else:
            # Run to home
            self.player.sprite.speed.x -= dt * 4.33

        # Flip Tye based on movement dir
        self.player.sprite.flip_sprite = self.player.sprite.speed.x > 0

        # Reveal text
        cutscene_end_time = 23
        text_reveal_time = 18
        if self.timer >= text_reveal_time:
            # Opacity should range from 0 to 1
            opacity = (self.timer - text_reveal_time) / (
                cutscene_end_time - text_reveal_time
            )

            if opacity < 1 / 5:
                self.font_disp = config.BIG_FONT.render(
                    "Run Away", False, (255, 255, 255)
                )
            elif opacity < 2 / 5:
                self.font_disp = config.BIG_FONT.render(
                    "Run Away >", False, (255, 255, 255)
                )
            elif opacity < 3 / 5:
                self.font_disp = config.BIG_FONT.render(
                    "Run Away ->", False, (255, 255, 255)
                )
            elif opacity < 4 / 5:
                self.font_disp = config.BIG_FONT.render(
                    "Run Away -->", False, (255, 255, 255)
                )
            else:
                self.font_disp = config.BIG_FONT.render(
                    "Run Away --->", False, (255, 255, 255)
                )

            self.font_disp.set_alpha(opacity * 255)  # Set opacity of text

            # Draw font onto the render surface
            self.render_surface.blit(self.font_disp, (40, 10))

        # End game
        if self.timer >= cutscene_end_time:
            pygame.quit()
            exit()

        # Set frame of house based on player position
        dist_factor = self.player.sprite.rect.x - self.home.sprite.rect.x - 85
        if dist_factor > 100:
            self.home.sprite.set_frame_by_percent(0)
        else:
            self.home.sprite.set_frame_by_percent((100 - dist_factor) / 100)
        self.home.sprite.set_frame_by_percent(self.player.sprite.rect.x)

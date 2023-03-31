from pathlib import Path

import config
import pygame

from core.camera import CameraGroup

from core.entity import Entity, AnimatedEntity, Hazard

from core.player import Player

from core.enemy import Grunt
from core.enemy import Flying

from core.portal import Portal
from core.NPC import NPC
from pytmx.util_pygame import load_pygame
from utils.tools import debug

from core.shop import Shop


class Level:
    def __init__(self, level_path, stats) -> None:
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
        self.home = pygame.sprite.GroupSingle()
        self.is_end_cutscene = False
        self.coins = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()

        self.in_shop = False
        self.shop = None    
        
        self.stats = stats
        # TODO create dictionary with all player possessions and attributes to pass down?
        # self.items = {coins :0, }

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

        try:
            for obj in tmx_data.get_layer_by_name("Interactables"):
                # Load portals
                if obj.type == "Portal":
                    Portal(
                        [self.all_sprites, self.portals],
                        None,
                        (obj.x, obj.y),
                        colour="blue",
                        level_path="run_away/resources/levels/level_"+obj.name[0:obj.name.find("_")].lower()+".tmx"
                    )
                if self.is_end_cutscene:
                    if getattr(obj, "class") == "Home":
                        from core.home import Home
                        Home(
                            [self.all_sprites, self.home],
                            None,
                            (obj.x, obj.y)
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
                    "./run_away/resources/gfx/player/",
                    speed=120,
                    gravity=275,
                    jump_speed=175,
                    coins = self.stats["coins"]
                )
            elif obj.name == "Start:ForceLeft":
                AnimatedEntity(
                    [self.all_sprites, self.player],
                    [self.collidable_sprites],
                    (obj.x, obj.y),
                    "./run_away/resources/gfx/player/",
                    speed=60, gravity=275
                ).direction = pygame.Vector2(-1, 0)
                self.is_end_cutscene = True
                self.player.sprite.status = "run"



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
                        colour=grunt_colour
                    )
                elif obj.type == "Flying":
                    Flying(
                        [self.all_sprites, self.enemies],
                        [self.collidable_sprites, self.player],
                        self.player,
                        (obj.x, obj.y),
                        speed=100
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
        
        if self.is_end_cutscene: self.update_end_cutscene(dt)

        scaled_display = pygame.transform.scale(
            self.render_surface,
            (self.display_surface.get_width(), self.display_surface.get_height()),
        )

        # Handle end cutscene
        if self.is_end_cutscene:
            self.display_surface.blit(scaled_display, (0, 150))
        else:
            self.display_surface.blit(scaled_display, (0, 0))
            # TODO update entire stats dictionary at once?
            self.stats["coins"] = self.player.sprite.coins

        self.check_coins()
        
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
            debug(f"Player Coins: {self.player.sprite.coins}", 200)
            self.check_portals()
        self.check_portals()
        pygame.display.flip()
        return self.check_portals()

    

    def update_end_cutscene(self, dt):

        # Create timer if doesn't exist
        if not hasattr(self, "timer"):
                self.timer = dt
        else:
            # Update timer based on delta-time
            self.timer += dt

        # Set Tye's speed
        if self.player.sprite.speed.x < 0:
            # RUN AWAY
            self.player.sprite.speed.x -= dt*20
        else:
            # Run to home
            self.player.sprite.speed.x -= dt*4.33

        # Flip Tye based on movement dir
        self.player.sprite.flip_sprite = self.player.sprite.speed.x > 0

        # Reveal text
        cutscene_end_time = 23
        text_reveal_time = 18
        if self.timer >= text_reveal_time:

            # Opacity should range from 0 to 1
            opacity = (self.timer - text_reveal_time)/(cutscene_end_time-text_reveal_time)

            if opacity < 1/5:
                self.font_disp = config.BIG_FONT.render("Run Away", False, (255, 255, 255))
            elif opacity < 2/5:
                self.font_disp = config.BIG_FONT.render("Run Away >", False, (255, 255, 255))
            elif opacity < 3/5:
                self.font_disp = config.BIG_FONT.render("Run Away ->", False, (255, 255, 255))
            elif opacity < 4/5:
                self.font_disp = config.BIG_FONT.render("Run Away -->", False, (255, 255, 255))
            else:
                self.font_disp = config.BIG_FONT.render("Run Away --->", False, (255, 255, 255))

            self.font_disp.set_alpha(opacity*255) # Set opacity of text

            # Draw font onto the render surface
            self.render_surface.blit(self.font_disp, (40,10))

        # End game 
        if self.timer >= cutscene_end_time:
            pygame.quit()
            exit()

        # Set frame of house based on player position
        dist_factor = (self.player.sprite.rect.x - self.home.sprite.rect.x-85)
        if dist_factor > 100:
            self.home.sprite.set_frame_by_percent(0)
        else:
            self.home.sprite.set_frame_by_percent((100-dist_factor)/100)
        self.home.sprite.set_frame_by_percent(self.player.sprite.rect.x)
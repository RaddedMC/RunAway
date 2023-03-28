from pathlib import Path

import config
import pygame
from core.camera import CameraGroup
from core.entity import Entity
from core.player import Player
from core.enemy import Grunt
from core.portal import Portal
from core.entity import AnimatedEntity
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
        self.portals = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.home = pygame.sprite.GroupSingle()
        self.is_end_cutscene = False

        self.import_assets(level_path)

    def resize_render_surface(self):
        self.render_surface = pygame.Surface(config.RENDER_AREA)

    # Load level items
    def import_assets(self, level_path):
        tmx_data = load_pygame(
            Path(level_path).resolve()
        )
        # print(dir(tmx_data))
        # print(tmx_data.layers)

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
                        Entity(
                            [self.all_sprites, self.collidable_sprites],
                            self.collidable_sprites,
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
                        )
                    elif layer.name == "Top Spikes":
                        Entity(
                            [self.all_sprites, self.collidable_sprites],
                            self.collidable_sprites,
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
                        )
                    elif layer.name == "Left Spikes":
                        Entity(
                            [self.all_sprites, self.collidable_sprites],
                            self.collidable_sprites,
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
                        )
                    elif layer.name == "Right Spikes":
                        Entity(
                            [self.all_sprites, self.collidable_sprites],
                            self.collidable_sprites,
                            (x * config.TILE_SIZE, y * config.TILE_SIZE),
                            surf,
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

            # print(dir(layer))  # DEBUG

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
                    jump_speed=175
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
                if getattr(obj,"class") == "Grunt":
                    Grunt(
                        [self.all_sprites, self.enemies],
                        [self.collidable_sprites, self.player],
                        (obj.x, obj.y),
                        speed=40,
                        gravity=100, # FIXME: hardcoded for now, make world property?
                        colour=grunt_colour
                    )
        except ValueError:
            # This level probably has no enemies
            pass


        for obj in tmx_data.get_layer_by_name("Interactables"):
            # Load portals
            if getattr(obj,"class") == "Portal":
                Portal(
                    [self.all_sprites, self.portals],
                    None,
                    (obj.x, obj.y),
                    colour="blue",
                    level_path="run_away/resources/levels/level_"+obj.name[0:obj.name.find("_")].lower()+".tmx"
                )
            # Load home if available
            from core.home import Home
            if getattr(obj,"class") == "Home":
                Home(
                    [self.all_sprites, self.home],
                    None,
                    (obj.x, obj.y)
                )
        
        
    def check_portals(self):
        grpcollide = pygame.sprite.groupcollide(self.player, self.portals, False, False)
        if self.player.sprite in grpcollide:
            return grpcollide[self.player.sprite][0]
        else: return False

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

        # Handle end cutscene
        if self.is_end_cutscene:
            self.update_end_cutscene(dt)
            self.display_surface.blit(scaled_display, (0, 150))
        else:
            self.display_surface.blit(scaled_display, (0, 0))
        
        if config.DEBUG_UI:
            debug(self.player.sprite.status)
            debug(f"Direction: {self.player.sprite.direction}", 40)
            debug(f"Speed: {self.player.sprite.speed}", 60)
            debug(f"Colliding: {pygame.sprite.spritecollide(self.player.sprite, self.collidable_sprites, False)}", 80)
            debug(f"On Ground: {self.player.sprite.on_ground}", 100)
            debug(f"Buffer: {self.player.sprite.pixels_buffer}", 120)
            debug(f"Position: ({self.player.sprite.rect.x}, {self.player.sprite.rect.y})", 140)

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
        if self.timer >= 19:

            # Opacity should range from 0 to 1
            opacity = (self.timer - 19)/4

            # Create font if it doesn't exist
            if not hasattr(self, "end_font"):
                self.end_font = pygame.font.Font("run_away/resources/font/Renogare-Regular.otf", 128)
                self.font_disp = self.end_font.render("Run Away", False, (255, 255, 255))

            self.font_disp.set_alpha(opacity*255) # Set opacity of text

            # Draw font onto the render surface
            self.display_surface.blit(self.font_disp, (0,10))

        # End game 
        if self.timer >= 23:
            pygame.quit()
            exit()

        # Set frame of house based on player position
        dist_factor = (self.player.sprite.rect.x - self.home.sprite.rect.x-85)
        if dist_factor > 100:
            self.home.sprite.set_frame_by_percent(0)
        else:
            self.home.sprite.set_frame_by_percent((100-dist_factor)/100)
        self.home.sprite.set_frame_by_percent(self.player.sprite.rect.x)
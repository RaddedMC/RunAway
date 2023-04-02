import pygame
import os
from pathlib import Path
import config
import math

class Background():

    def __init__(
            self,
            path_from_tiled: str,
            parallax_x: float,
            parallax_y: float,
            world_width: float,
            world_height: float,
            bg_width: float,
            bg_height: float
    ):

        # Import things
        self.image = pygame.image.load(Path(os.getcwd() + "/" + config.BASE_PATH + "/" + path_from_tiled[3:]))
        self.image = pygame.transform.scale(self.image, config.RENDER_AREA)

        # Save additional properties
        self.parallax = pygame.Vector2()
        self.parallax.x = parallax_x
        self.parallax.y = parallax_y
        self.world_width = world_width
        self.world_height = world_height
        self.bg_width = bg_width
        self.bg_height = bg_height


    def draw(
            self,
            offset_x: float,
            offset_y: float,
            screen_to_draw: pygame.Surface
    ):
        x_pos = 0
        blits_x = 1
        y_pos = 0
        blits_y = 1
        if not self.parallax.x == 1:
            x_pos = offset_x*self.parallax.x
            blits_x = math.ceil(1/self.parallax.x*(self.world_width/self.bg_width))
        if not self.parallax.y == 1:
            y_pos = offset_y*self.parallax.y
            blits_y = math.ceil(1/self.parallax.y*(self.world_height/self.bg_height))

        for x_blit in range(-blits_x, blits_x):
            for y_blit in range(-blits_y, blits_y):
                screen_to_draw.blit(
                    source = self.image,
                    dest=(x_pos+(x_blit*self.world_width), y_pos+(y_blit*self.world_height))
                )
import math
from pathlib import Path

import pygame

from run_away import config


class Background:
    def __init__(
        self,
        path_from_tiled: str,
        parallax_x: float,
        parallax_y: float,
        world_width: float,
        world_height: float,
        bg_width: float,
        bg_height: float,
        image_offset_x: float,
        image_offset_y: float,
    ):
        # Import things
        self.image = pygame.image.load(
            Path(str(config.BASE_PATH) + "/resources/" + path_from_tiled[3:])
        )
        self.image = pygame.transform.scale(self.image, config.RENDER_AREA)

        # Save additional properties
        self.parallax = pygame.Vector2()
        self.parallax.x = parallax_x
        self.parallax.y = parallax_y
        self.world_width = world_width
        self.world_height = world_height
        self.bg_width = bg_width
        self.bg_height = bg_height
        self.image_offset_x = image_offset_x
        self.image_offset_y = image_offset_y

    def draw(self, offset_x: float, offset_y: float, screen_to_draw: pygame.Surface):
        # 1 -- Pinned to corner of world
        # ------
        # ------
        # 0 -- Pinned to corner of camera

        # Defaults for parallax drawing. By default it will avoid tiling and pin to the top-left of the screen
        x_pos = 0
        blits_x = 1
        y_pos = 0
        blits_y = 1

        # If there is no pre-defined offset, enable tiling
        # If the parallax is not 1, pin to defined player offset
        # If it is 1, pin to world corner (0,0)

        # If the parallax is 1, there is no need to tile or offset since the background will be pinned to the corner of the world
        if not self.parallax.x == 1:
            # Positional offset of the background should be multiplied by parallax
            x_pos = offset_x * self.parallax.x

            # If parallax is 0, blit only once since pinned to camera
            # Disable tiling when there is a position offset
            if self.parallax.x == 0 or not self.image_offset_x == 0:
                blits_x = 1
            else:
                blits_x = math.ceil(
                    1 / self.parallax.x * (self.world_width / self.bg_width)
                )

        # Repeat above for y-coord
        if not self.parallax.y == 1:
            y_pos = offset_y * self.parallax.y
            if self.parallax.y == 0 or not self.image_offset_y == 0:
                blits_y = 1
            else:
                blits_y = math.ceil(
                    1 / self.parallax.y * (self.world_height / self.bg_height)
                )

        # Tiled blitting
        for x_blit in range(-blits_x, blits_x):
            for y_blit in range(-blits_y, blits_y):
                screen_to_draw.blit(
                    source=self.image,
                    dest=(
                        x_pos + (x_blit * self.world_width) + self.image_offset_x,
                        y_pos + (y_blit * self.world_height) + self.image_offset_y,
                    ),
                )

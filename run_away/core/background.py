import pygame
import os
from pathlib import Path
from config import BASE_PATH

class Background():

    def __init__(
            self,
            path_from_tiled: str,
            parallax_x: float,
            parallax_y: float
    ):

        # Import things
        self.image = pygame.image.load(Path(os.getcwd() + "/" + BASE_PATH + "/" + path_from_tiled[3:]))

        # Save additional properties
        self.parallax = pygame.Vector2(parallax_x, parallax_y)


    def draw(
            self,
            offset_x: float,
            offset_y: float,
            screen_to_draw: pygame.Surface
    ):
        offset = pygame.Vector2(offset_x*self.parallax.x, offset_y*self.parallax.y)
        screen_to_draw.blit(source=self.image, dest=offset)
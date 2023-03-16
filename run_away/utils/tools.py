# Contains common operations used by multiple classes

import pprint
from pathlib import Path
from typing import Optional

import pygame

from run_away import config

font = config.DEBUG_FONT


def import_folder():
    pass


def import_animations(folder_path: str):
    animations = {}

    for path in Path(folder_path).iterdir():
        if path.is_dir():
            animations.update({f"{path.name}": [child for child in path.iterdir()]})

    return animations


def debug(info, y: int = 10, x: Optional[int] = 10):
    """
    Create a simple debug panel to access information on the screen.

    Note: debug must be called after everything else has been drawn to the screen already.
    """
    display_surface = pygame.display.get_surface()
    debug_surface = font.render(str(info), True, config.RGB_WHITE)
    debug_rect = debug_surface.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surface, config.RGB_BLACK, debug_rect)
    display_surface.blit(debug_surface, debug_rect)


if __name__ == "__main__":  # DEBUG
    pprint.pprint(import_animations(Path("./run_away/resources/gfx/player/")))

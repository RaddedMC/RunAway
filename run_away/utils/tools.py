# Contains common operations used by multiple classes

import os
import pprint
from math import sin
from pathlib import Path
from typing import Optional

import pygame

from run_away import config

font = config.DEBUG_FONT


def import_folder(folder_path: str):
    folder_dict = {}

    for path in Path(folder_path).iterdir():
        if path.is_dir():
            folder_dict.update({f"{path.name}": [child for child in path.iterdir()]})

    return folder_dict


def get_sounds_by_key(key: str):
    path = "./run_away/resources/sfx/" + key + "/"
    files = os.listdir(path)
    return [pygame.mixer.Sound(path + file) for file in files]


def import_animations(folder_path: str):
    return import_folder(folder_path)


def get_wave_value():
    value = sin(pygame.time.get_ticks())
    if value >= 0:
        return 255
    else:
        return 0


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

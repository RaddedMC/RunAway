# Contains common operations used by multiple classes

import os
from math import sin
from pathlib import Path
from typing import Union

import pygame

from run_away import config

font = config.DEBUG_FONT


def import_folder(folder_path: Union[str, Path]) -> dict[str, list[Path]]:
    if type(folder_path) is str:
        folder_path = Path(folder_path)

    folder_dict = {}

    for path in folder_path.iterdir():
        if path.is_dir():
            folder_dict.update({f"{path.name}": [child for child in path.iterdir()]})

    return folder_dict


def get_sounds_by_key(key: str) -> list[pygame.mixer.Sound]:
    path = config.SFX_PATH.joinpath(key)
    files = os.listdir(path)
    return [pygame.mixer.Sound(path.joinpath(file)) for file in files]


def import_animations(folder_path: Union[str, Path]):
    return import_folder(folder_path)


def get_wave_value() -> int:
    value = sin(pygame.time.get_ticks())
    if value >= 0:
        return 255
    else:
        return 0


def debug(info, y: int = 10, x: int = 10) -> None:
    """
    Create a simple debug panel to access information on the screen.

    Note: must be called after everything else has been drawn to the screen already.
    """
    display_surface = pygame.display.get_surface()
    debug_surface = font.render(str(info), True, config.RGB_WHITE)
    debug_rect = debug_surface.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surface, config.RGB_BLACK, debug_rect)
    display_surface.blit(debug_surface, debug_rect)

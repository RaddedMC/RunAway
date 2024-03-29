import sys
from pathlib import Path

import pygame

# Run Away
# By James Nicholls, Kelsey Kloosterman, Lukas Adie, and Sharaf Syed
# Made for SE 2250, made for life

### THIS FILE contains key settings for the game that can be adjusted. ###

### DEBUG FLAG ###
DEBUG_VERBOSE_LOGGING = False
DEBUG_UI = False
DEBUG_ZOOM = False
DEBUG_SHOW_HITBOXES = False
DEBUG_STATS = False

### FOLDER PATHS ###
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    # App is running in a PyInstaller bundle
    BASE_PATH = Path(sys._MEIPASS)
else:
    # App is running in a normal Python process
    BASE_PATH = Path.cwd().absolute().joinpath("run_away")

RESOURCES_PATH = BASE_PATH.joinpath("resources")
FONT_PATH = RESOURCES_PATH.joinpath("font")
GFX_PATH = RESOURCES_PATH.joinpath("gfx")
LEVELS_PATH = RESOURCES_PATH.joinpath("levels")
MUSIC_PATH = RESOURCES_PATH.joinpath("music")
SFX_PATH = RESOURCES_PATH.joinpath("sfx")


### GAME WORLD ###
TILE_SIZE = 16

### ENTITY CONSTANTS ###
ENEMY_COLOUR_LOOKUP = {
    "rain": "red",
    "wind": "yellow",
    "lightning": "green",
    "snow": "blue",
}
HAZARD_DATA = {
    "damage": 1,
    "top": {"scale": (0, -0.65), "offset": pygame.math.Vector2(0, -6)},
    "bottom": {"scale": (0, -0.65), "offset": pygame.math.Vector2(0, 6)},
    "left": {"scale": (-0.65, 0), "offset": pygame.math.Vector2(-6, 0)},
    "right": {"scale": (-0.65, 0), "offset": pygame.math.Vector2(6, 0)},
}
PLAYER_DATA = {
    "animation_speed": 9,
    "jump_speed": 175,
    "gravity": 275,
    "stats": {
        "speed": 120,
        "health": 10,
        "damage": 10,
        "strength": 10,
        "agility": 10,
        "coins": 100 if DEBUG_STATS else 0,
    },
}
ENEMY_DATA = {
    "grunt": {"animation_speed": 6, "stats": {"speed": 40, "health": 10, "damage": 1}},
    "flying": {
        "animation_speed": 6,
        "stats": {"speed": 100, "health": 5, "damage": 1},
    },
    "shooter": {
        "animation_speed": 6,
        "stats": {
            "speed": 0,
            "health": 10,
            "damage": 1,
            "p_speed": 40,
            "p_health": 1,
            "p_damage": 1,
        },
    },
}
PROJECTILE_DATA = {
    "rain": {
        "animation_speed": 14,
        "scale": (-0.3, -0.5),
        "offset": {
            "left": pygame.math.Vector2(0, -5),
            "right": pygame.math.Vector2(0, -5),
        },
    },
    "wind": {
        "animation_speed": 18,
        "scale": (0, 0),
        "offset": {
            "left": pygame.math.Vector2(0, 3),
            "right": pygame.math.Vector2(0, 3),
        },
    },
    "lightning": {
        "animation_speed": 24,
        "scale": (0, -0.5),
        "offset": {
            "left": pygame.math.Vector2(0, -5),
            "right": pygame.math.Vector2(0, -5),
        },
    },
    "snow": {
        "animation_speed": 10,
        "scale": (-0.45, -0.65),
        "offset": {
            "left": pygame.math.Vector2(-20, -8),
            "right": pygame.math.Vector2(20, -8),
        },
    },
}
NPC_DIALOGUE = {
    "RAIN": ["You have to leave this place!"],
    "WIND": ["Be careful of the winged ones"],
    "SNOW": ["Brrrrrrrr"],
    "LIGHTNING": ["Why are we in the tropics?"],
}
WEAPON_DATA = {
    "damage": 4,
    "offset": {
        "left": pygame.math.Vector2(-12, 0),
        "right": pygame.math.Vector2(12, 0),
    },
    "scale": (0, 1.1),
}
PORTAL_DATA = {"animation_speed": 10, "dialogue": ["Press Z to Travel"]}
LEVEL_DATA = {}
SHOP_DATA = {"price": 7}

### CONTROLS ###
KEYS_LEFT = [pygame.K_LEFT, pygame.K_a]
KEYS_RIGHT = [pygame.K_RIGHT, pygame.K_d]
KEYS_UP = [pygame.K_UP, pygame.K_w]
KEYS_DOWN = [pygame.K_DOWN, pygame.K_s]
KEYS_QUIT = [pygame.K_ESCAPE]
KEYS_INTERACT = [pygame.K_j, pygame.K_z]
KEYS_ATTACK = [pygame.K_x, pygame.K_k]

### COLOURS ###
RGB_BLACK = (0, 0, 0)
RGB_WHITE = (255, 255, 255)

### RENDERING ###
"""
All computers and displays are different. Pygame seems to be finicky with its handling
of frame-independent movement. The default FPS is 120hz, as that matches (or doubles)
the system refresh rate of everyone's development machines. If you have performance
issues, reduce this to 60hz or lower (I recommend keeping it a factor of 2 however)
"""
FPS = 120
DISP_ZOOM = 1.1
RENDER_AREA = (256 * DISP_ZOOM, 144 * DISP_ZOOM)  # 16:9 aspect ratio


def change_render_area():
    global RENDER_AREA
    global DISP_ZOOM
    if DISP_ZOOM <= 0:
        DISP_ZOOM = 0.0000000000001
    RENDER_AREA = (256 * DISP_ZOOM, 144 * DISP_ZOOM)  # 16:9 aspect ratio


### FONTS ###
pygame.font.init()
DEBUG_FONT = pygame.font.Font(None, 30)

GAME_FONT = pygame.font.Font(FONT_PATH.joinpath("BitFont.ttf"), 30)
MENU_FONT = pygame.font.Font(FONT_PATH.joinpath("BitFont.ttf"), 10)
BIG_FONT = pygame.font.Font(FONT_PATH.joinpath("ROGFonts-Regular.otf"), 20)

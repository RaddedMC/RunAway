import sys

import config
import pygame
from core.level import Level, LevelType
from core.player import Player
from utils.tools import get_sounds_by_key


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Run Away")
        self.clock = pygame.time.Clock()
        self.player_stats = {"health": config.PLAYER_DATA["stats"]["health"] ,"strength": config.PLAYER_DATA["stats"]["strength"] ,"agility": config.PLAYER_DATA["stats"]["agility"] ,"coins": config.PLAYER_DATA["stats"]["coins"] }
        self.level = Level(LevelType.RAIN, self.player_stats)
        self.running = True
        self.lightning_clear = False
        self.snow_clear = False
        self.wind_clear = False
        self.load_sfx = get_sounds_by_key("portal")

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if True in [keys[key] for key in config.KEYS_QUIT]:
                        self.running = False

                # For mouse wheel zooming
                if event.type == pygame.MOUSEWHEEL:
                    if config.DEBUG_ZOOM:
                        config.DISP_ZOOM += event.y * 2 / 3 * 0.1
                        print(event.y)
                        config.change_render_area()
                        self.level.resize_render_surface()
                        print(config.RENDER_AREA)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 2:
                        if config.DEBUG_ZOOM:
                            config.DISP_ZOOM = 1.1
                            config.change_render_area()
                            self.level.resize_render_surface()
                            print(config.RENDER_AREA)

            dt = self.clock.tick(config.FPS) / 1000
            next_level = self.level.run(dt)
            pygame.display.flip()
            if next_level:
                self.load_sfx[0].play()
                if next_level.target_level is LevelType.HUB:
                    if self.level.kind is LevelType.LIGHTNING:
                        self.lightning_clear = True
                    elif self.level.kind is LevelType.SNOW:
                        self.snow_clear = True
                    elif self.level.kind is LevelType.WIND:
                        self.wind_clear = True

                if self.lightning_clear and self.snow_clear and self.wind_clear:
                    if next_level.target_level is LevelType.HUB:
                        next_level.target_level = LevelType.HUB_RAIN_ACCESS

                self.level = Level(next_level.target_level, self.player_stats)

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    game = Game()
    game.run()

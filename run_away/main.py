import sys

import pygame

import config
from core.level import Level, LevelType
from core.player import Player


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Run Away")
        self.clock = pygame.time.Clock()
        self.player_stats = {"coins": 1}
        self.level = Level(LevelType.RAIN.value, self.player_stats)
        self.running = True
        self.lightning_clear = False
        self.snow_clear = False
        self.wind_clear = False

    def run(self):
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
                if next_level.level_path is LevelType.HUB:
                    if self.level.lvl_path is LevelType.LIGHTNING:
                        self.lightning_clear = True
                    elif self.level.lvl_path is LevelType.SNOW:
                        self.snow_clear = True
                    elif self.level.lvl_path is LevelType.WIND:
                        self.wind_clear = True

                if self.lightning_clear and self.snow_clear and self.wind_clear:
                    if next_level.level_path is LevelType.HUB:
                        next_level.level_path = LevelType.HUB_RAIN_ACCESS

                self.level = Level(next_level.level_path, self.player_stats)

            print(f"({self.wind_clear}, {self.lightning_clear}, {self.snow_clear})")

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    game = Game()
    game.run()

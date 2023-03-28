import sys

import pygame

import config
from core.level import Level
from core.player import Player
from utils.tools import get_sounds_by_key


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Run Away")
        self.clock = pygame.time.Clock()
        self.player_stats = {"coins": 1}
        self.level = Level(config.STARTING_LEVEL_PATH, self.player_stats)
        self.running = True
        self.lightning_clear = False
        self.snow_clear = False
        self.wind_clear = False
        self.load_sfx = get_sounds_by_key("portal")

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
                        config.DISP_ZOOM += event.y*2/3*0.1
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
                if "hub" in next_level.level_path:
                    if "lightning" in self.level.lvl_path:
                        self.lightning_clear = True
                    elif "snow" in self.level.lvl_path:
                        self.snow_clear = True 
                    elif "wind" in self.level.lvl_path:
                        self.wind_clear = True

                if self.lightning_clear and self.snow_clear and self.wind_clear:
                    if "hub" in next_level.level_path:
                        next_level.level_path = "run_away/resources/levels/level_hub_rainaccess.tmx"

                self.level = Level(next_level.level_path, self.player_stats)

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    game = Game()
    game.run()

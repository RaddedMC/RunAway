import sys

import pygame

import config
from core.level import Level


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.display_surface = pygame.display.set_mode((256,144), pygame.SCALED + pygame.FULLSCREEN)
        pygame.display.set_caption("Run Away")
        self.clock = pygame.time.Clock()
        self.level = Level("run_away/resources/levels/level_wind.tmx")
        self.running = True

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
            self.level.run(dt)
            pygame.display.flip()

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    game = Game()
    game.run()

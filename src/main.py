import sys

import pygame

import config
from core.level import Level


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.display_screen = pygame.display.set_mode((256,144), pygame.SCALED + pygame.FULLSCREEN)
        pygame.display.set_caption("Run Away")
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            dt = self.clock.tick(config.FPS) / 1000
            self.level.run(dt)
            pygame.display.flip()

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    game = Game()
    game.run()

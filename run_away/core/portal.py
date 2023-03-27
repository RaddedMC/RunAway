import pygame
from core.NPC import NPC

class Portal(NPC):
    def __init__(
            self,
            groups: pygame.sprite.Group,
            collidable_sprites: pygame.sprite.Group,
            pos: tuple,
            colour: str,
            level_path: str,
            dialogue  = ["Press Z to Travel"]           
    ):
        root_dir = "./run_away/resources/gfx/objects/portal" + "/" + colour
        self.level_path = level_path
        super().__init__(groups, collidable_sprites, pos, root_dir, dialogue, speed=0, gravity=0)
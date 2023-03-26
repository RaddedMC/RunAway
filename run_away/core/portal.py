import pygame
from core.entity import InteractableEntity

class Portal(InteractableEntity):
    def __init__(
            self,
            groups: pygame.sprite.Group,
            collidable_sprites: pygame.sprite.Group,
            pos: tuple,
            colour: str,
            level_path: str
            
    ):
        root_dir = "./run_away/resources/gfx/objects/portal" + "/" + colour
        self.level_path = level_path
        super().__init__(groups, collidable_sprites, pos, root_dir, speed=0, gravity=0)
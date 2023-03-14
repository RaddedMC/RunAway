from pathlib import Path
from typing import Optional

import pygame

from utils import tools


class Entity(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        pos: tuple,
        image: pygame.Surface,
        speed: Optional[int] = 0,
    ):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed

    def update(self, dt: float):
        self.move(dt)
        self.collision()

    def move(self, dt: float):
        pass

    def collision(self):
        pass


class AnimatedEntity(Entity):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        pos: tuple,
        root_dir: str,
    ):
        self.status = "idle"  # TODO: hardcoded for now
        self.animation_speed = 0.15  # TODO: hardcoded for now
        self.frame_index = 0
        self.animations = tools.import_animations(root_dir)
        image = pygame.image.load(self.animations[self.status][self.frame_index]).convert_alpha()
        super().__init__(groups, pos, image)

    def animate(self, dt: float):
        animation = self.animations[self.status]

        # Increment to the next frame in the animation
        self.frame_index += self.animation_speed

        # Reached the end of the animation, return to the beginning
        if self.frame_index >= len(animation):
            # TODO: use % operator instead
            self.frame_index = 0

        # Set the image for the current frame
        # TODO: implement left/right directions
        image_path = animation[int(self.frame_index)]
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt: float):
        self.move(dt)
        self.collision()
        self.animate(dt)

    def get_status():
        """
        Determine and set the entity's status
        """
        pass


class InteractableEntity(Entity):
    def __init__(self, pos, image, name, groups):
        super().__init__(pos, image, groups)
        self.name = name


class Portal(InteractableEntity):
    pass


class NPC(InteractableEntity):
    pass

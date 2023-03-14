from pathlib import Path
from typing import Optional

import pygame

from utils import tools


class Entity(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple,
        image: pygame.Surface,
        speed: Optional[int] = 0,
    ):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed
        self.direction = pygame.math.Vector2(0, 0)
        self.collidable_sprites = collidable_sprites

    def move(self, dt: float):
        # TODO: rounding?
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

    def collision(self):
        """
        Handle collision between this entity and a group of possible entities it can
        collide with.

        Note: collisions that occur while this entity is stationary are ignored.
        """
        # TODO: actually update the entity's position in response to collisions

        # The entity was moving when the collision occurred
        if self.direction.magnitude() != 0 and pygame.sprite.spritecollideany(
            self, self.collidable_sprites
        ):
            # The entity was moving horizontally
            if self.direction.x != 0:
                if self.direction.x > 0:  # Moving right
                    pass
                elif self.direction.x < 0:  # Moving left
                    pass

            # The entity was moving vertically
            if self.direction.y != 0:
                if self.direction.y < 0:  # Moving up
                    pass
                elif self.direction.y > 0:  # Moving down
                    pass

    def update(self, dt: float):
        self.move(dt)
        self.collision()


class AnimatedEntity(Entity):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple,
        root_dir: str,
        speed: Optional[int] = 0,
    ):
        self.status = "idle"  # FIXME: hardcoded for now
        self.animation_speed = 0.15  # FIXME: hardcoded for now
        self.frame_index = 0
        self.animations = tools.import_animations(root_dir)
        image = pygame.image.load(
            self.animations[self.status][self.frame_index]
        ).convert_alpha()
        super().__init__(groups, collidable_sprites, pos, image, speed)

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
        super().update(dt)
        self.animate(dt)


class InteractableEntity(Entity):
    def __init__(self, pos, image, name, groups):
        super().__init__(pos, image, groups)
        self.name = name


class Portal(InteractableEntity):
    pass


class NPC(InteractableEntity):
    pass

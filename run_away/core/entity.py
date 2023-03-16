from typing import Optional

import pygame
from utils.tools import import_animations


class Entity(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple,
        image: pygame.Surface,
    ):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.collidable_sprites = collidable_sprites
        self.pixels_buffer = pygame.math.Vector2(0, 0)

    def update(self, dt: float):
        pass

class AnimatedEntity(Entity):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple,
        root_dir: str,
        speed: float = 0,
        gravity: float = 0
    ):
        self.status = "idle"  # FIXME: hardcoded for now
        self.animation_speed = 0.15  # FIXME: hardcoded for now
        self.frame_index = 0
        # Movement vars
        self.walk_speed = speed
        self.gravity = gravity
        self.vert_speed = 0
        self.walk_direction = 0

        # Animations
        self.animations = import_animations(root_dir)
        image = pygame.image.load(
            self.animations[self.status][self.frame_index]
        ).convert_alpha()
        super().__init__(groups, collidable_sprites, pos, image)

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
        self.move(dt)
        #self.collision()
        self.animate(dt)

    def move(self, dt: float):

        # Handle gravity
        self.vert_speed += dt*self.gravity

        # Determine pixels to move
        self.pixels_buffer.x += self.walk_direction * self.walk_speed * dt # Based on walk speed and deltatime
        self.pixels_buffer.y += self.vert_speed * dt

        # Pixel buffer to ensure that the rectangle only moves given whole number input:
        # Add (x/y)*speed*dir to x and y buffer
        # if abs(buffer) for a coord is greater than 1
        # Move 1 and subtract buffer by 1
        import math
        if (math.floor(self.pixels_buffer.x) > 1):
            self.rect.move_ip(math.floor(self.pixels_buffer.x),0)
            self.pixels_buffer.x -= math.floor(self.pixels_buffer.x)
        elif (math.floor(self.pixels_buffer.x) < -1):
            self.rect.move_ip(math.floor(self.pixels_buffer.x),0)
            self.pixels_buffer.x -= math.floor(self.pixels_buffer.x)

        if (math.floor(self.pixels_buffer.y) > 1):
            self.rect.move_ip(0, math.floor(self.pixels_buffer.y))
            self.pixels_buffer.y -= math.floor(self.pixels_buffer.y)
        elif (math.floor(self.pixels_buffer.y) < -1):
            self.rect.move_ip(0, math.floor(self.pixels_buffer.y))
            self.pixels_buffer.y -= math.floor(self.pixels_buffer.y)

    def collision(self):
        """
        Handle collision between this entity and a group of possible entities it can
        collide with.

        Note: collisions that occur while this entity is stationary are ignored.
        """
        # TODO: actually update the entity's position in response to collisions
        # I think all we need to do here is just set speed in a direction to 0 if a collision occurs -- James

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
    


class InteractableEntity(Entity):
    def __init__(self, pos, image, name, groups):
        super().__init__(pos, image, groups)
        self.name = name


class Portal(InteractableEntity):
    pass


class NPC(InteractableEntity):
    pass

from typing import Optional

import pygame
from utils.tools import import_animations

class Directions():
    LEFT = -1
    RIGHT = 1

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
        pos: tuple, #FIXME: Should be vector2?
        root_dir: str,
        speed: float = 0,
        gravity: float = 0
    ):
        self.status = "idle"
        self.animation_speed = 18  # FIXME: hardcoded for now
        self.frame_index = 0
        # Movement vars
        self.walk_speed = speed
        self.gravity = gravity
        self.vert_speed = 0
        self.walk_direction = 0
        self.flip_sprite = False # False = right, True = left

        # Animations
        self.animations = import_animations(root_dir)
        from config import DEBUG_VERBOSE_LOGGING
        if DEBUG_VERBOSE_LOGGING:
            print(self.animations)
        image = pygame.image.load(
            self.animations[self.status][self.frame_index]
        ).convert_alpha()
        super().__init__(groups, collidable_sprites, pos, image)

    def animate(self, dt: float):
        animation = self.animations[self.status]

        # Increment to the next frame in the animation
        self.frame_index += self.animation_speed * dt
        self.frame_index = self.frame_index % len(animation)

        # Set the image for the current frame
        # TODO: implement left/right directions
        image_path = animation[int(self.frame_index)]
        self.image = pygame.image.load(image_path)
        if self.flip_sprite:
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt: float):
        super().update(dt)
        self.collision()
        self.move(dt)
        self.animate(dt)

    def move(self, dt: float):

        # Handle gravity
        if not self.test_collide_down():
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
        Handle directional collision between this entity and a group of possible entities it can
        collide with.

        Note: collisions that occur while this entity is stationary are ignored.
        """
        # Test all collisions
        # If left collides:
        if self.test_collide_left():
            # x speed should be >=0
            if self.walk_direction < 0:
                self.walk_direction = 0
                

        # If right collides:
        if self.test_collide_right():
            # x speed should be <=0
            if self.walk_direction > 0:
                self.walk_direction = 0
        
        # If up collides:
        if self.test_collide_up():
            # y speed should be >= 0
            if self.vert_speed < 0:
                self.vert_speed = 0

        # If down collides:
        if self.test_collide_down():
            # y speed should be <= 0
            if self.vert_speed > 0:
                self.vert_speed = 0

    def test_collide(self, dir = pygame.Vector2):
        # Move by dir
        self.rect.move_ip(dir.x, dir.y)
        
        # Test collision
        collided = not pygame.sprite.spritecollideany(self, self.collidable_sprites) == None

        # undo movement
        self.rect.move_ip(-dir.x, -dir.y)

        # Return true if collide, false if not collide
        from config import DEBUG_VERBOSE_LOGGING
        if DEBUG_VERBOSE_LOGGING:
            print(f"Collision {dir}: {collided} | Vertical speed = {self.vert_speed} | Horiz direction = {self.walk_direction}")
        return collided

    def test_collide_left(self):
        return self.test_collide(pygame.Vector2(-1,0))
    
    def test_collide_right(self):
        return self.test_collide(pygame.Vector2(1,0))

    def test_collide_up(self):
        return self.test_collide(pygame.Vector2(0,-1))

    def test_collide_down(self):
        return self.test_collide(pygame.Vector2(0,1))
    


class InteractableEntity(Entity):
    def __init__(self, pos, image, name, groups):
        super().__init__(pos, image, groups)
        self.name = name


class Portal(InteractableEntity):
    pass


class NPC(InteractableEntity):
    pass

import math
from typing import Optional

import pygame
import random
from utils.tools import import_animations

import config


class Directions:
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
        self.hitbox = self.rect.copy()
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
        gravity: float = 0,
    ):
        # Movement
        self.speed = pygame.math.Vector2(speed, 0)
        self.gravity = gravity
        self.max_gravity = gravity
        self.direction = pygame.math.Vector2(0, 0)
        self.flip_sprite = False  # False = right, True = left

        # Animations
        self.status = "idle"  # FIXME: hardcoded for now
        self.animation_speed = 18  # FIXME: hardcoded for now
        self.frame_index = 0
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

        # Reached the end of the animation, return to the beginning
        self.frame_index = self.frame_index % len(animation)

        # Set the image for the current frame
        image_path = animation[int(self.frame_index)]
        self.image = pygame.image.load(image_path)
        if self.flip_sprite:
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt: float):
        super().update(dt)
        self.apply_gravity(dt)
        self.move(dt)
        self.animate(dt)

    def apply_gravity(self, dt):
        # if not self.on_ground:
        self.speed.y += self.gravity * dt

        # Limit how fast the entity can fall
        if self.speed.y > self.max_gravity:
            self.speed.y = self.max_gravity

        # FIXME: use a less arbitrary number
        if self.speed.y > 30:
            self.direction.y = 1

    def move(self, dt: float):
        # Calculate the position the entity will attempt to move to
        self.pixels_buffer.x += self.direction.x * self.speed.x * dt
        self.pixels_buffer.y += self.speed.y * dt

        if self.pixels_buffer.x != 0:
            # Calculate the horizontal position that the entity can actually move to
            self.pixels_buffer.x = self.horizontal_collision(self.pixels_buffer.x)

            # Perform the horizontal movement
            self.rect.move_ip(math.floor(self.pixels_buffer.x), 0)
            self.hitbox.move_ip(math.floor(self.pixels_buffer.x), 0)

            self.pixels_buffer.x -= math.floor(self.pixels_buffer.x)

        if self.pixels_buffer.y != 0:
            # Calculate the vertical position that the entity can actually move to
            self.pixels_buffer.y = self.vertical_collision(self.pixels_buffer.y)

            # Perform the vertical movement
            self.rect.move_ip(0, math.floor(self.pixels_buffer.y))
            self.hitbox.move_ip(0, math.floor(self.pixels_buffer.y))

            self.pixels_buffer.y -= math.floor(self.pixels_buffer.y)

        if self.direction.y != 0:
            self.on_ground = False

    def horizontal_collision(self, dx: float):
        if dx != 0:
            # Move a copy of the entity and check for collisions
            test_rect = self.hitbox.copy()
            test_rect.move_ip(math.floor(dx), 0)
            collided = self.test_collisions(test_rect)

            # The proposed move caused collisions
            if len(collided) > 0:
                self.speed.x = 0

                if dx > 0:  # Moving right
                    # The x-coordinate of the closest (leftmost) entity we collided with
                    min_left = min([sprite.left for sprite in collided])

                    # The max distance that this entity can move without causing collision
                    return min_left - self.hitbox.right
                else:  # Moving left
                    # The x-coordinate of the closest (rightmost) entity we collided with
                    max_right = max([sprite.right for sprite in collided])

                    # The max distance that this entity can move without causing collision
                    return max_right - self.hitbox.left
            else:
                # No collisions, the entity can move the full distance
                return dx

    def vertical_collision(self, dy: float):
        if dy != 0:
            # Move a copy of the entity and check for collisions
            test_rect = self.hitbox.copy()
            test_rect.move_ip(0, math.floor(dy))
            collided = self.test_collisions(test_rect)

            # The proposed move caused collisions
            if len(collided) > 0:
                self.speed.y = 0

                if dy < 0:  # Moving up
                    # The y-coordinate of the closest (bottommost) entity we collided with
                    lowest_bottom = max([sprite.bottom for sprite in collided])

                    # The max distance that this entity can move without causing collision
                    return lowest_bottom - self.hitbox.top
                else:
                    self.direction.y = 0
                    self.speed.y = 0
                    if self.on_ground == False:
                        try:
                            random.choice(self.land_sounds).play()
                        except AttributeError:
                            pass
                    self.on_ground = True

                    # The y-coordinate of the closest (topmost) entity we collided with
                    max_top = min([sprite.top for sprite in collided])

                    # The max distance that this entity can move without causing collision
                    return max_top - self.hitbox.bottom
            else:
                # No collisions, the entity can move the full distance
                return dy

    def test_collisions(self, test_rect: pygame.Rect):
        collided = []
        if type(self.collidable_sprites) == list:
            for sprite_list in self.collidable_sprites:
                for sprite in sprite_list:
                    if test_rect.colliderect(sprite.hitbox):
                        collided.append(sprite.hitbox)
        else:
            for sprite in self.collidable_sprites:
                if test_rect.colliderect(sprite.hitbox):
                    collided.append(sprite.hitbox)

        return collided


class InteractableEntity(AnimatedEntity):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple,  # FIXME: Should be vector2?
        root_dir: str,
        speed: float = 0,
        gravity: float = 0,
    ):
        super().__init__(groups, collidable_sprites, pos, root_dir, speed, gravity)


class Portal(InteractableEntity):
    pass


class NPC(InteractableEntity):
    pass


class Hazard(Entity):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple,
        image: pygame.Surface,
        type: str,
    ):
        super().__init__(groups, collidable_sprites, pos, image)
        self.type = type
        self.hitbox = (
            self.rect.copy()
            .inflate(
                tuple(
                    l * r
                    for l, r in zip(
                        self.rect.size, config.HAZARD_DATA[self.type]["scale"]
                    )
                )
            )
            .move(config.HAZARD_DATA[self.type]["offset"])
        )

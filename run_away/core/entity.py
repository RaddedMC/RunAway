from __future__ import annotations

import math
import random
from pathlib import Path
from typing import Optional, Union

import config
import pygame
from utils.tools import get_wave_value, import_animations


class Block(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        pos: Union[tuple[int, int], tuple[int, int, int, int]],
        image: Optional[pygame.Surface] = None,
    ):
        super().__init__(groups)

        if image is None:  # pos is expected to have extra width and height dimensions
            self.rect = pygame.rect.Rect(pos)
        else:
            self.image = image
            self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.copy()
        

class Entity(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        collidable_sprites: Optional[list[pygame.sprite.Group]],
        pos: tuple[int, int],
        image: pygame.Surface,
        speed: float = 0,
        gravity: float = 0
    ) -> None:
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()
        self.collidable_sprites = collidable_sprites
        self.vulnerable = True  # FIXME: temp fix for AttributeError
        self.on_ground = False  # FIXME: temp fix for AttributeError

        # Movement
        self.pixels_buffer = pygame.math.Vector2(0, 0)
        self.speed = pygame.math.Vector2(speed, 0)
        self.gravity = gravity
        self.max_gravity = gravity
        self.direction = pygame.math.Vector2(0, 0)
        self.on_ground = False

    def apply_gravity(self, dt: float) -> None:
        # if not self.on_ground:
        self.speed.y += self.gravity * dt

        # Limit how fast the entity can fall
        if self.speed.y > self.max_gravity:
            self.speed.y = self.max_gravity

        # FIXME: use a less arbitrary number
        if self.speed.y > 30:
            self.direction.y = 1

    def move(self, dt: float) -> None:
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

    def horizontal_collision(self, dx: float) -> Union[None, float]:
        from core.enemy import Enemy, Projectile
        from core.player import Player
        from core.weapon import Weapon

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
                    min_left = min([sprite.hitbox.left for sprite in collided])

                    if type(self) is Player or isinstance(self, Enemy):
                        self.check_damage(collided, min_left, "left")

                    if type(self) is Projectile:
                        self.kill()

                    # The max distance that this entity can move without causing collision
                    return min_left - self.hitbox.right
                else:  # Moving left
                    # The x-coordinate of the closest (rightmost) entity we collided with
                    max_right = max([sprite.hitbox.right for sprite in collided])

                    if type(self) is Player or isinstance(self, Enemy):
                        self.check_damage(collided, max_right, "right")
                        

                    if type(self) is Projectile:
                        self.kill()

                    # The max distance that this entity can move without causing collision
                    return max_right - self.hitbox.left
            else:
                # No collisions, the entity can move the full distance
                return dx

    def vertical_collision(self, dy: float) -> Union[None, float]:
        from core.enemy import Enemy
        from core.player import Player
        from core.weapon import Weapon

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
                    lowest_bottom = max([sprite.hitbox.bottom for sprite in collided])

                    if type(self) is Player or isinstance(self, Enemy):
                        self.check_damage(collided, lowest_bottom, "bottom")

                    # The max distance that this entity can move without causing collision
                    return lowest_bottom - self.hitbox.top
                else:
                    self.direction.y = 0
                    self.speed.y = 0
                    if not self.gravity == 0 and self.on_ground is False:
                        try:
                            random.choice(self.land_sounds).play()
                        except AttributeError:
                            pass

                    self.on_ground = True

                    # The y-coordinate of the closest (topmost) entity we collided with
                    max_top = min([sprite.hitbox.top for sprite in collided])

                    if type(self) is Player or isinstance(self, Enemy):
                        self.check_damage(collided, max_top, "top")

                    # The max distance that this entity can move without causing collision
                    return max_top - self.hitbox.bottom
            else:
                # No collisions, the entity can move the full distance
                return dy

    def test_collisions(self, test_rect: pygame.Rect) -> list[Entity]:
        collided = []
        if type(self.collidable_sprites) == list:
            for sprite_list in self.collidable_sprites:
                for sprite in sprite_list:
                    if test_rect.colliderect(sprite.hitbox):
                        collided.append(sprite)
        else:
            for sprite in self.collidable_sprites:
                if test_rect.colliderect(sprite.hitbox):
                    collided.append(sprite)

        return collided

    def check_damage(
        self, collided: list[Entity], rect_pos: int, rect_pos_attr: str
    ) -> None:
        if rect_pos_attr == "top":
            s = next(
                (sprite for sprite in collided if sprite.hitbox.top == rect_pos), None
            )
        elif rect_pos_attr == "bottom":
            s = next(
                (sprite for sprite in collided if sprite.hitbox.bottom == rect_pos),
                None,
            )
        elif rect_pos_attr == "left":
            s = next(
                (sprite for sprite in collided if sprite.hitbox.left == rect_pos), None
            )
        else:
            s = next(
                (sprite for sprite in collided if sprite.hitbox.right == rect_pos), None
            )

        from core.enemy import Enemy, Projectile
        from core.player import Player

        # The player collided with...
        if type(self) is Player:
            # ...a Hazard or an Enemy
            if type(s) is Hazard or isinstance(s, Enemy):
                self.apply_damage(s.get_damage())

            # ...a Projectile
            if type(s) is Projectile:
                s.kill()

        # (type) collided with the player
        if type(s) is Player:
            # (Enemy)
            if isinstance(self, Enemy):
                s.apply_damage(self.get_damage())

            # (Projectile)
            if type(self) is Projectile:
                self.kill()

    def update(self, dt: float) -> None:
        if not self.gravity == 0:
            self.apply_gravity(dt)
        self.move(dt)


class AnimatedEntity(Entity):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        collidable_sprites: Optional[list[pygame.sprite.Group]],
        pos: tuple[int, int],
        root_dir: Union[str, Path],
        animation_speed: int = 18,  # FIXME: should this even have a default?
        speed: float = 0,
        gravity: float = 0,
    ) -> None:
        # Animations
        self.status = "idle"  # FIXME: hardcoded for now
        self.animation_speed = animation_speed
        self.frame_index = 0
        self.animations = import_animations(root_dir)
        self.flip_sprite = False  # False = right, True = left

        from config import DEBUG_VERBOSE_LOGGING

        if DEBUG_VERBOSE_LOGGING:
            print(self.animations)

        image = pygame.image.load(
            self.animations[self.status][self.frame_index]
        ).convert_alpha()

        super().__init__(groups, collidable_sprites, pos, image, speed, gravity)

    def animate(self, dt: float) -> None:
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

        # Make the player flicker to indicate an invincibility frame
        if not self.vulnerable:
            alpha = get_wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self, dt: float) -> None:
        super().update(dt)
        self.animate(dt)


class InteractableEntity(AnimatedEntity):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        collidable_sprites: Optional[list[pygame.sprite.Group]],
        pos: tuple[int, int],
        root_dir: Union[str, Path],
        animation_speed: int,
        speed: float = 0,
        gravity: float = 0,
    ) -> None:
        super().__init__(
            groups, collidable_sprites, pos, root_dir, animation_speed, speed, gravity
        )


class Hazard(Entity):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        collidable_sprites: Optional[list[pygame.sprite.Group]],
        pos: tuple[int, int],
        image: pygame.Surface,
        damage: float,
        kind: str,
    ) -> None:
        super().__init__(groups, collidable_sprites, pos, image)
        self.kind = kind
        self.hitbox = (
            self.rect.copy()
            .inflate(
                tuple(
                    l * r
                    for l, r in zip(
                        self.rect.size, config.HAZARD_DATA[self.kind]["scale"]
                    )
                )
            )
            .move(config.HAZARD_DATA[self.kind]["offset"])
        )
        self.damage = damage

    def get_damage(self) -> float:
        return self.damage

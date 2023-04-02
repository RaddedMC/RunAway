import os
import random
from pathlib import Path
from typing import Union

import config
import pygame
from config import DEBUG_VERBOSE_LOGGING
from core.entity import AnimatedEntity, Entity
from core.player import Player


class Enemy(AnimatedEntity):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        collidable_sprites: list[pygame.sprite.Group],
        pos: tuple[int, int],
        root_dir: Union[str, Path],
        animation_speed: int,
        speed: float,
        gravity: float,
        health: float,
        damage: float,
        player: Player,
    ) -> None:
        super().__init__(
            groups,
            collidable_sprites,
            pos,
            root_dir,
            animation_speed,
            speed,
            gravity,
        )
        self.max_speed = speed
        self.health = health
        self.damage = damage
        self.player = player

    def run_behaviour(self) -> None:
        """
        Called every frame, figures out what the enemy does (are they attacking the player? changing movement direction? etc)
        """
        pass

    def get_damage(self) -> float:
        """
        Calculates the amount of damage this enemy should deal.
        """
        return config.LEVEL_DATA["damage_factor"][
            0
        ]  # TODO: [0] is temporary until I figure out how to track level progress

    def check_death(self):
        if self.health <= 0:
            pass  # FIXME: DIE

    def update(self, dt: float) -> None:
        super().update(dt)
        self.run_behaviour()
        self.check_death()

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

        if type(s) is Player:
            s.apply_damage(self.get_damage())

        # TODO: handle weapon damage here


class Grunt(Enemy):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        collidable_sprites: list[pygame.sprite.Group],
        pos: tuple[int, int],
        root_dir: Union[str, Path],
        animation_speed: int,
        speed: float,
        gravity: float,
        health: float,
        damage: float,
        player: Player,
        colour: str = "red",
    ) -> None:
        if type(root_dir) is Path:
            root_dir = root_dir.joinpath(colour)
        else:
            root_dir = os.path.join(root_dir, colour)

        super().__init__(
            groups,
            collidable_sprites,
            pos,
            root_dir,
            animation_speed,
            speed,
            gravity,
            health,
            damage,
            player,
        )
        self.direction.x = -1

        if DEBUG_VERBOSE_LOGGING:
            print(
                f"Grunt spawned!: speed:{speed}| colour:{colour}| pos:{pos}| gravity:{gravity}"
            )

    def update(self, dt: float) -> None:
        if DEBUG_VERBOSE_LOGGING:
            print(f"Grunt - {self.direction.x}, {self.speed.x}")
        super().update(dt)
        self.handle_directions(dt)

    def handle_directions(self, dt: float) -> None:
        # Handle sprite direction
        self.flip_sprite = self.direction.x == 1

        # Revert the collision system's speed reset
        # TODO: handle differently..?
        if self.speed.x == 0:
            self.speed.x = self.max_speed

        # If it stops moving, it is likely because it can't move
        if self.pixels_buffer.x == 0:
            # Horizontal collision
            self.direction.x *= -1


class Flying(Enemy):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        collidable_sprites: list[pygame.sprite.Group],
        pos: tuple[int, int],
        root_dir: Union[str, Path],
        animation_speed: int,
        speed: float,
        health: float,
        damage: float,
        player: Player,
    ) -> None:
        super().__init__(
            groups,
            collidable_sprites,
            pos,
            root_dir,
            animation_speed,
            speed,
            0,
            health,
            damage,
            player,
        )
        self.direction.x = 1
        self.launched = False

    def update(self, dt: float) -> None:
        super().update(dt)
        if DEBUG_VERBOSE_LOGGING:
            print(f"Frame: {int(self.frame_index)} ", end="")

        if int(self.frame_index) == 5 and not self.launched:
            self.launch()
            self.launched = True
        else:
            self.launched = False
            if self.speed.x < 0:
                self.speed.x += 50 * dt
                if self.speed.x > 0:
                    self.speed.x = 0
            elif self.speed.x > 0:
                self.speed.x -= 50 * dt
                if self.speed.x < 0:
                    self.speed.x = 0

            if self.speed.y < 0:
                self.speed.y += 50 * dt
                if self.speed.y > 0:
                    self.speed.y = 0
            elif self.speed.y > 0:
                self.speed.y -= 50 * dt
                if self.speed.y < 0:
                    self.speed.y = 0

            if DEBUG_VERBOSE_LOGGING:
                print(f"Not a launch frame. ({self.speed.x}, {self.speed.y})")

    def launch(self) -> None:
        x_diff = abs(self.player.rect.x - self.rect.x)
        x_launch = 0
        if x_diff < self.max_speed:
            x_launch = x_diff * 2
        else:
            x_launch = self.max_speed

        y_diff = abs(self.player.rect.y - self.rect.y)
        y_launch = 0
        if y_diff < self.max_speed:
            y_launch = y_diff * 2
        else:
            y_launch = self.max_speed

        if self.player.rect.x > self.rect.x:
            self.speed.x = x_launch + random.randrange(0, self.max_speed * 0.1)
        elif self.player.rect.x < self.rect.x:
            self.flip_sprite = True
            self.speed.x = -(x_launch + random.randrange(0, self.max_speed * 0.1))
        else:
            self.speed.x = 0

        if self.player.rect.y > self.rect.y:
            self.speed.y = y_launch + random.randrange(0, self.max_speed * 0.1)
        elif self.player.rect.y < self.rect.y:
            self.speed.y = -(y_launch + random.randrange(0, self.max_speed * 0.1))
        else:
            self.speed.y = 0

        if DEBUG_VERBOSE_LOGGING:
            print(f"Launch! ({self.speed.x}, {self.speed.y})")


class Shooter(Enemy):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        collidable_sprites: list[pygame.sprite.Group],
        pos: tuple[int, int],
        root_dir: Union[str, Path],
        animation_speed: int,
        speed: float,
        gravity: float,
        health: float,
        projectile_speed: float,
        projectile_health: float,
        projectile_damage: float,
        player: Player,
        colour: str = "red",
    ) -> None:
        if type(root_dir) is Path:
            root_dir = root_dir.joinpath(colour)
        else:
            root_dir = os.path.join(root_dir, colour)

        super().__init__(
            groups,
            collidable_sprites,
            pos,
            root_dir,
            animation_speed,
            speed,
            gravity,
            health,
            0,  # TODO: do we want player to take damage when colliding with this enemy?
            player,
        )
        self.projectile_speed = projectile_speed
        self.projectile_health = projectile_health  # TODO: might not end up using, see below
        self.projectile_damage = projectile_damage

        # Shooter will shoot projectiles non-stop
        # Do we want shooter to only shoot new projectile once old one has "died" or shoot after a delay?
        # Should the projectiles themselves have health? (so that player can counter them)
        # Should shooter only shoot when visible on screen?

        # Shooter needs to be able to spawn facing a specified direction
        # TODO: add direction custom property to each Projectile in Tiled: "right", "left"
        # Should shooter be able to "follow" the player? (i.e., flip direction to face the player)

        # TODO: "kill" projectile after it collides with something (add code to entity collision methods)
        # TODO: get & apply damage if it collided with a Player

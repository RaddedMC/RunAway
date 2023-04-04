import os
import random
from pathlib import Path
from typing import Callable, Optional, Union

import config
import pygame
from config import DEBUG_VERBOSE_LOGGING
from core.entity import AnimatedEntity
from core.player import Player
from core.weapon import Weapon


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

        # Invincibility frames
        self.vulnerable = True
        self.invulnerable_duration = 500  # TODO: move to config?
        self.hurt_time = None

    def cooldowns(self) -> None:
        now = pygame.time.get_ticks()

        if not self.vulnerable:
            # Invincibility frame has expired
            if now - self.hurt_time >= self.invulnerable_duration:
                self.vulnerable = True
                self.hurt_time = None

    def run_behaviour(self) -> None:
        """
        Called every frame, figures out what the enemy does (are they attacking the player? changing movement direction? etc)
        """
        pass

    def get_damage(self) -> float:
        """
        Returns the amount of damage this enemy should deal.
        """
        return self.damage

    def apply_damage(self, amount: int) -> None:
        if self.vulnerable:
            self.health -= amount
            self.vulnerable = False
            self.hurt_time = pygame.time.get_ticks()
            # random.choice(self.hit_sounds).play()
            # random.choice(self.iframe_sfx).play()

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.player.get_coin()  # TODO: spawn a coin instead

    def check_weapon_damage(self) -> None:
        if self.player.weapon is not None:
            collided = pygame.sprite.groupcollide(
                pygame.sprite.GroupSingle(self),
                pygame.sprite.GroupSingle(self.player.weapon),
                False,
                False,
            )
            if collided:
                self.apply_damage(self.player.weapon.get_damage())

    def update(self, dt: float) -> None:
        self.cooldowns()
        super().update(dt)
        self.run_behaviour()
        self.check_weapon_damage()
        self.check_death()


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

    def update(self, dt: float) -> None:
        if DEBUG_VERBOSE_LOGGING:
            print(f"Grunt - {self.direction.x}, {self.speed.x}")
        super().update(dt)
        self.handle_directions(dt)


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
            self.flip_sprite = False
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
        damage: float,
        projectile_speed: float,
        projectile_health: float,
        projectile_damage: float,
        player: Player,
        create_projectile: Callable,
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

        # Projectile
        self.colour = colour
        self.projectile_speed = projectile_speed
        self.projectile_health = projectile_health
        self.projectile_damage = projectile_damage
        self.create_projectile = create_projectile

        # Track enemy states/actions
        self.can_shoot = True
        self.attack_delay = 2750  # TODO: move to config?
        self.attack_time = None

    def cooldowns(self) -> None:
        super().cooldowns()

        if self.attack_time is None:
            return

        now = pygame.time.get_ticks()

        # We are able to shoot another projectile
        if now - self.attack_time >= self.attack_delay:
            self.can_shoot = True
            self.attack_time = None

    def check_direction(self):
        if self.rect.x < self.player.rect.x:  # Player is to the right of the enemy
            self.direction.x = 1
            self.flip_sprite = False
        else:  # Player is to the left of the enemy
            self.direction.x = -1
            self.flip_sprite = True

    def shoot(self) -> None:
        # Spawn the projectile, make it move in the same direction that the shooter is facing
        if self.can_shoot:
            self.create_projectile(
                self.rect.topleft,
                config.GFX_PATH.joinpath("objects", "projectiles"),
                self.projectile_speed,
                self.projectile_health,
                self.projectile_damage,
                self.get_direction_str(),
                self.colour,
            )
            self.attack_time = pygame.time.get_ticks()
            self.can_shoot = False

    def update(self, dt: float) -> None:
        super().update(dt)
        self.check_direction()
        self.shoot()


class Projectile(Enemy):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        collidable_sprites: list[pygame.sprite.Group],
        pos: tuple[int, int],
        root_dir: Union[str, Path],
        animation_speed: Optional[int],
        speed: float,
        health: float,
        damage: float,
        player: Player,
        direction: str,
        kind: str,
    ) -> None:
        if type(root_dir) is Path:
            root_dir = root_dir.joinpath(kind)
        else:
            root_dir = os.path.join(root_dir, kind)

        if animation_speed is None:
            animation_speed = config.PROJECTILE_DATA[kind]["animation_speed"]

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
        self.rect.move_ip(config.PROJECTILE_DATA[kind]["offset"][direction])
        self.hitbox = self.rect.copy().inflate(
            tuple(
                l * r
                for l, r in zip(self.rect.size, config.PROJECTILE_DATA[kind]["scale"])
            )
        )

        if direction == "left":
            self.direction.x = -1
            self.flip_sprite = True
        elif direction == "right":
            self.direction.x = 1
            self.flip_sprite = False

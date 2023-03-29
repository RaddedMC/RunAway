import pygame
from core.entity import AnimatedEntity
from core.entity import Directions
from config import DEBUG_VERBOSE_LOGGING, LEVEL_DATA


class Enemy(AnimatedEntity):
    def __init__(
        self,
        health,
        damage,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple,
        root_dir: str,
        level_progress: tuple[bool, bool, bool],
        speed: float = 0,
        gravity: float = 0,
    ):
        super().__init__(groups, collidable_sprites, pos, root_dir, speed, gravity)
        self.health = health
        self.damage = damage
        self.level_progress = level_progress
        # TODO: enemy stats will be multiplied by a decimal factor for each level (e.g., 2nd level * 1.25, 3rd * 1.5, etc.)

    def update(self, dt: float):
        super().update(dt)
        self.run_behaviour()
        self.check_death()

    def run_behaviour(self):
        """
        Called every frame, figures out what the enemy does (are they attacking the player? changing movement direction? etc)
        """
        pass

    def get_damage(self):
        """
        Calculates the amount of damage this enemy should deal.
        """
        return LEVEL_DATA["damage_factor"][self.level_progress.count(True)]

    def check_death(self):
        if self.health <= 0:
            pass  # FIXME: DIE


class Grunt(Enemy):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple,
        level_progress: tuple[bool, bool, bool],
        speed: float = 5,
        gravity: float = 0,
        colour: str = "red",
    ):
        health = 10  # FIXME: change once we have a combat system
        damage = 10  # FIXME: ^
        super().__init__(
            health,
            damage,
            groups,
            collidable_sprites,
            pos,
            f"./run_away/resources/gfx/enemies/grunt/{colour}",
            level_progress,
            speed,
            gravity,
        )
        self.animation_speed = 6
        self.direction.x = -1
        self.desired_speed = speed

        if DEBUG_VERBOSE_LOGGING:
            print(
                f"Grunt spawned!: speed:{speed}| colour:{colour}| pos:{pos}| gravity:{gravity}"
            )

    def update(self, dt: float):
        if DEBUG_VERBOSE_LOGGING:
            print(f"Grunt - {self.direction.x}, {self.speed.x}")
        super().update(dt)
        self.handle_directions(dt)

    def handle_directions(self, dt: float):
        # Handle sprite direction
        self.flip_sprite = self.direction.x == 1

        # Revert the collision system's speed reset
        # TODO: handle differently..?
        if self.speed.x == 0:
            self.speed.x = self.desired_speed

        # If it stops moving, it is likely because it can't move
        if self.pixels_buffer.x == 0:
            # Horizontal collision
            self.direction.x *= -1


class Flying(Enemy):
    pass

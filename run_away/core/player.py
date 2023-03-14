from pathlib import Path

import config
import pygame

from core.entity import AnimatedEntity
from utils import tools


class Player(AnimatedEntity):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple,
        root_dir: str,
    ):
        super().__init__(groups, collidable_sprites, pos, root_dir)

        # Player stats
        self.stats = None
        self.skills = None

        # Weapon
        self.weapon_data = None

        # Track player states/actions
        self.attacking = False
        self.attack_cooldown = None

        # Invincibility frames
        self.vulnerable = True
        self.invulnerable_duration = None
        self.hurt_time = None

    def get_inputs(self):
        """
        Handle inputs from the user
        """
        # Get the keys that were pressed
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_w]:
            self.jump()
        else:
            # Not moving
            self.direction.update(0, 0)

    def jump(self):
        """
        Make the player jump
        """
        self.direction.y = -1

    def get_status(self):
        """
        Determine and set the status of the player (e.g. idle, attack, move)
        """
        pass

    def check_death(self):
        pass

    def update(self, dt):
        self.get_inputs()
        super().update(dt)
        self.check_death()

import pygame
from core.entity import AnimatedEntity
import config


class Player(AnimatedEntity):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple,
        root_dir: str,
        speed: int, # Measured in PIXELS per SECOND
        gravity: int
    ):
        super().__init__(groups, collidable_sprites, pos, root_dir, speed, gravity)

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
        keys_pressed = False

        if True in [keys[key] for key in config.KEYS_RIGHT]:
            self.walk_direction = 1
        elif True in [keys[key] for key in config.KEYS_LEFT]:
            self.walk_direction = -1
        else:
            self.walk_direction = 0
        
        if True in [keys[key] for key in config.KEYS_UP]:
            self.jump()

    def jump(self):
        """
        Make the player jump
        """
        self.vert_speed = -50

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

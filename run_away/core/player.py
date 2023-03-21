import pygame
from core.entity import AnimatedEntity
import config
from core.entity import Directions


class Player(AnimatedEntity):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple,
        root_dir: str,
        speed: int, # Measured in PIXELS per SECOND
        gravity: int,
        jump_speed: int
    ):
        super().__init__(groups, collidable_sprites, pos, root_dir, speed, gravity)

        # Player stats
        self.stats = {"speed": speed}  # FIXME: temp
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

        # Movement
        self.jump_speed = jump_speed
        self.on_ground = False

    def get_inputs(self):
        """
        Handle inputs from the user
        """
        # Get the keys that were pressed
        keys = pygame.key.get_pressed()

        # Modify speed and direction of the player based on the key that was pressed
        if True in [keys[key] for key in config.KEYS_RIGHT]:
            # self.status = "run"  # FIXME: disabled temporarily until we add the idle, run animations for the new sprite (make sure that both images have the same height!)
            self.direction.x = 1
            self.speed.x = self.stats["speed"]
            self.flip_sprite = False
        elif True in [keys[key] for key in config.KEYS_LEFT]:
            # self.status = "run"
            self.direction.x = -1
            self.speed.x = self.stats["speed"]
            self.flip_sprite = True
        else:
            self.status = "idle"
            self.direction.x = 0
            self.speed.x = 0
        
        if True in [keys[key] for key in config.KEYS_UP]:
            self.jump()

    def jump(self):
        """
        Make the player jump
        """
        if self.on_ground:
            self.speed.y = -self.jump_speed
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
        # self.get_status()
        super().update(dt)
        self.check_death()

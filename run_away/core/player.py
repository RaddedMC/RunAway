import random

import config
import pygame
from core.entity import AnimatedEntity, Directions, Hazard
from utils.tools import get_sounds_by_key


class Player(AnimatedEntity):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple,
        root_dir: str,
        speed: int,  # Measured in PIXELS per SECOND
        gravity: int,
        jump_speed: int,
        coins: int
    ):
        self.config = config.PLAYER_DATA
        self.stats = self.config["stats"]
        super().__init__(
            groups,
            collidable_sprites,
            pos,
            root_dir,
            self.stats["speed"],
            self.config["gravity"],
        )

        # Animation
        self.animation_speed = self.config[
            "animation_speed"
        ]  # FIXME: hardcoded for now, this should be loaded from the config

        # Player stats
        self.health = self.stats["health"]
        self.damage = self.stats["damage"]
        self.skills = None

        # Movement
        self.spawn_point = pos
        self.jump_speed = self.config["jump_speed"]
        self.on_ground = False

        # Weapon
        self.weapon_data = None

        # Track player states/actions
        self.attacking = False
        self.attack_cooldown = None

        # Invincibility frames
        self.on_hazard = False
        self.vulnerable = True
        self.invulnerable_duration = 500  # Note: time is in milliseconds
        self.hurt_time = None

        # SFX
        self.jump_sounds = get_sounds_by_key("player_jump")
        self.land_sounds = get_sounds_by_key("player_land")
        self.coin_sounds = get_sounds_by_key("coin_pick")
        self.hit_sounds  = get_sounds_by_key("player_hit")
        self.iframe_sfx  = get_sounds_by_key("player_iframe_tone")
        self.die_sfx     = get_sounds_by_key("player_die")

        self.coins = coins


    def get_inputs(self):
        """
        Handle inputs from the user
        """
        # Get the keys that were pressed
        keys = pygame.key.get_pressed()

        # Modify speed and direction of the player based on the key that was pressed
        if True in [keys[key] for key in config.KEYS_RIGHT]:
            self.status = "run"
            self.direction.x = 1
            self.speed.x = self.stats["speed"]
            self.flip_sprite = False
        elif True in [keys[key] for key in config.KEYS_LEFT]:
            self.status = "run"
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
            random.choice(self.jump_sounds).play()
            self.speed.y = -self.jump_speed
            self.direction.y = -1

    def get_status(self):
        """
        Determine and set the status of the player (e.g. idle, attack, move)
        """
        pass

    def cooldowns(self):
        now = pygame.time.get_ticks()

        if not self.vulnerable:
            # Invincibility frame has expired
            if now - self.hurt_time >= self.invulnerable_duration:
                self.vulnerable = True
                self.hurt_time = None

    def get_damage(self):
        if self.vulnerable and self.on_hazard:
            self.health -= 1  # FIXME: hardcoded for now
            self.vulnerable = False
            self.on_hazard = False
            self.hurt_time = pygame.time.get_ticks()
            random.choice(self.hit_sounds).play()
            random.choice(self.iframe_sfx).play()

    def check_death(self):
        """
        Determine if the player is dead.
        """
        if self.health <= 0:
            print("You Died!")

            self.die_sfx[0].play()

            # FIXME: make a respawn method that resets all booleans, position, etc.?

            # Reset player status
            self.status = "idle"
            self.on_ground = False
            self.on_hazard = False
            self.vulnerable = True

            # Restore player health back to its base value
            self.health = self.stats["health"]

            # Respawn the player at the start of the current level
            self.rect.topleft = self.spawn_point
            self.hitbox.topleft = self.spawn_point

    def get_coin(self):
        self.coins += 1
        self.coin_sounds[0].play()
    
    def spend_coins(self, price: int):
        self.coins -= price

    def update(self, dt):
        self.get_inputs()
        self.cooldowns()
        # self.get_status()
        super().update(dt)
        self.get_damage()
        self.check_death()

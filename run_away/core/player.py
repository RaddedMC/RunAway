import random
from pathlib import Path
from typing import Union

import config
import pygame
from core.entity import AnimatedEntity, Hazard
from utils.tools import get_sounds_by_key


class Player(AnimatedEntity):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        collidable_sprites: list[pygame.sprite.Group],
        pos: tuple[int, int],
        root_dir: Union[str, Path],
        animation_speed: int,
        speed: float,  # Measured in PIXELS per SECOND
        gravity: float,
        health: float,
        damage: float,
        jump_speed: int,
        coins: int = 0,
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
        # Player stats
        self.health = health
        self.max_health = health
        self.damage = damage
        self.skills = None

        # Movement
        self.spawn_point = pos
        self.max_speed = speed
        self.jump_speed = jump_speed
        self.on_ground = False

        # Weapon
        self.weapon_data = None

        # Track player states/actions
        self.attacking = False
        self.attack_cooldown = None
        self.attack_time = None

        # Invincibility frames
        self.vulnerable = True
        self.invulnerable_duration = 500  # Note: time is in milliseconds
        self.hurt_time = None

        # SFX
        self.jump_sounds = get_sounds_by_key("player_jump")
        self.land_sounds = get_sounds_by_key("player_land")
        self.coin_sounds = get_sounds_by_key("coin_pick")
        self.hit_sounds = get_sounds_by_key("player_hit")
        self.iframe_sfx = get_sounds_by_key("player_iframe_tone")
        self.die_sfx = get_sounds_by_key("player_die")

        self.coins = coins

    def get_inputs(self) -> None:
        """
        Handle inputs from the user
        """
        # Get the keys that were pressed
        keys = pygame.key.get_pressed()

        # Modify speed and direction of the player based on the key that was pressed
        if True in [keys[key] for key in config.KEYS_RIGHT]:
            self.status = "run"
            self.direction.x = 1
            self.speed.x = self.max_speed
            self.flip_sprite = False
        elif True in [keys[key] for key in config.KEYS_LEFT]:
            self.status = "run"
            self.direction.x = -1
            self.speed.x = self.max_speed
            self.flip_sprite = True
        else:
            self.status = "idle"
            self.direction.x = 0
            self.speed.x = 0

        if True in [keys[key] for key in config.KEYS_UP]:
            self.jump()

        if True in [keys[key] for key in config.KEYS_INTERACT]:
            self.status = "interacting"

    def jump(self) -> None:
        """
        Make the player jump
        """
        if self.on_ground:
            random.choice(self.jump_sounds).play()
            self.speed.y = -self.jump_speed
            self.direction.y = -1

    def get_status(self) -> None:
        """
        Determine and set the status of the player (e.g. idle, attack, move)
        """
        pass

    def cooldowns(self) -> None:
        now = pygame.time.get_ticks()

        if not self.vulnerable:
            # Invincibility frame has expired
            if now - self.hurt_time >= self.invulnerable_duration:
                self.vulnerable = True
                self.hurt_time = None

    def apply_damage(self, amount: int) -> None:
        if self.vulnerable:
            self.health -= amount
            self.vulnerable = False
            self.hurt_time = pygame.time.get_ticks()
            random.choice(self.hit_sounds).play()
            random.choice(self.iframe_sfx).play()

    def check_death(self) -> None:
        """
        Determine if the player is dead.
        """
        if self.health <= 0:
            print("You Died!")  # DEBUG

            self.die_sfx[0].play()

            # FIXME: make a respawn method that resets all booleans, position, etc.?

            # Reset player status
            self.status = "idle"
            self.on_ground = False
            self.vulnerable = True

            # Restore player health back to its base value
            self.health = self.max_health

            # Respawn the player at the start of the current level
            self.rect.topleft = self.spawn_point
            self.hitbox.topleft = self.spawn_point

    def get_coin(self) -> None:
        self.coins += 1
        self.coin_sounds[0].play()

    def spend_coins(self, price: int) -> None:
        self.coins -= price

    def update(self, dt) -> None:
        self.get_inputs()
        self.cooldowns()
        # self.get_status()
        super().update(dt)
        self.check_death()

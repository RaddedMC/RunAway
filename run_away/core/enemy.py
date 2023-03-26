import pygame
from core.entity import AnimatedEntity
from core.entity import Directions

class Enemy(AnimatedEntity):
    def __init__(self, health, damage,
                groups: pygame.sprite.Group,
                collidable_sprites: pygame.sprite.Group,
                pos: tuple,
                root_dir: str,
                speed: float = 0,
                gravity: float = 0,):
        super().__init__(groups, collidable_sprites, pos, root_dir, speed, gravity)
        self.health = health
        self.damage = damage

    def update(self, dt: float):
        super().update(dt)
        self.run_behaviour()
        self.check_death()

    def run_behaviour(self):
        """
        Called every frame, figures out what the enemy does (are they attacking the player? changing movement direction? etc)
        """
        pass

    def check_death(self):
        if self.health <= 0:
            pass #FIXME: DIE

class Grunt(Enemy):

    def __init__(self,
                groups: pygame.sprite.Group,
                collidable_sprites: pygame.sprite.Group,
                pos: tuple,
                root_dir: str,
                speed: float = 5,
                gravity: float = 0,
                colour: str = "red"):
        health = 10 #FIXME: change once we have a combat system
        damage = 10 #FIXME: ^
        self.root_dir = root_dir + "/" + colour
        super().__init__(health, damage, groups, collidable_sprites, pos, self.root_dir, speed, gravity)
        self.animation_speed = 6
        self.direction.x = -1
        self.desired_speed = speed

        from config import DEBUG_VERBOSE_LOGGING
        if DEBUG_VERBOSE_LOGGING:
            print(f"Grunt spawned!: speed:{speed}| colour:{colour}| pos:{pos}| gravity:{gravity}")

    def update(self, dt: float):
        print(f"Grunt - {self.direction.x}, {self.speed.x}")
        super().update(dt)
        self.handle_directions(dt)
    
    def handle_directions(self, dt:float):
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
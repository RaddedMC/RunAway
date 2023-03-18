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
        self.root_dir = self.root_dir + "/" + colour
        self.walk_direction = Directions.RIGHT
        super().__init__(health, damage, groups, collidable_sprites, pos, root_dir, speed, gravity)

    def run_behaviour(self):
        # Grunts are braindead bricks that move back and forth
        if self.test_collide_down():
            self.walk_direction *= -1

        if self.walk_direction == Directions.LEFT:
            if self.test_collide_left():
                self.walk_direction = Directions.RIGHT

        if self.walk_direction == Directions.RIGHT:
            if self.test_collide_right():
                self.walk_direction = Directions.LEFT

class Flying(Enemy):
    pass
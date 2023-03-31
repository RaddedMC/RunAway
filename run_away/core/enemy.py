import pygame
from core.entity import AnimatedEntity
from core.entity import Directions
from config import DEBUG_VERBOSE_LOGGING

import random

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
                speed: float = 5,
                gravity: float = 0,
                colour: str = "red"):
        health = 10 #FIXME: change once we have a combat system
        damage = 10 #FIXME: ^
        self.root_dir = "./run_away/resources/gfx/enemies/grunt" + "/" + colour
        super().__init__(health, damage, groups, collidable_sprites, pos, self.root_dir, speed, gravity)
        self.animation_speed = 6
        self.direction.x = -1
        self.desired_speed = speed

        if DEBUG_VERBOSE_LOGGING:
            print(f"Grunt spawned!: speed:{speed}| colour:{colour}| pos:{pos}| gravity:{gravity}")

    def update(self, dt: float):
        if DEBUG_VERBOSE_LOGGING:
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
    
    def __init__(self,
                  groups: pygame.sprite.Group,
                  collidable_sprites: pygame.sprite.Group,
                  target: pygame.sprite.GroupSingle,
                  pos: tuple,
                  speed: float = 5
                  ):
        health = 10 #FIXME: see grunt
        damage = 10
        self.root_dir = "./run_away/resources/gfx/enemies/flying/"
        super().__init__(health, damage, groups, collidable_sprites, pos, self.root_dir, speed, 0)
        self.animation_speed = 6
        self.direction.x = 1
        self.desired_speed = speed
        self.target = target
        self.launched = False
    
    def update(self, dt: float):
        super().update(dt)
        # print(f"Frame: {int(self.frame_index)} ", end="")

        if int(self.frame_index) == 5 and not self.launched:
            self.launch()
            self.launched = True
        else:
            self.launched = False
            if self.speed.x < 0:
                self.speed.x += 50*dt
                if self.speed.x > 0:
                    self.speed.x = 0
            elif self.speed.x > 0:
                self.speed.x -= 50*dt
                if self.speed.x < 0:
                    self.speed.x = 0

            if self.speed.y < 0:
                self.speed.y += 50*dt
                if self.speed.y > 0:
                    self.speed.y = 0
            elif self.speed.y > 0:
                self.speed.y -= 50*dt
                if self.speed.y < 0:
                    self.speed.y = 0

            
            # print(f"Not a launch frame. ({self.speed.x}, {self.speed.y})")

    def launch(self):
        x_diff = abs(self.target.sprite.rect.x - self.rect.x)
        x_launch = 0
        if x_diff < self.desired_speed:
            x_launch = x_diff*2
        else:
            x_launch = self.desired_speed

        y_diff = abs(self.target.sprite.rect.y - self.rect.y)
        y_launch = 0
        if y_diff < self.desired_speed:
            y_launch = y_diff*2
        else:
            y_launch = self.desired_speed

        if self.target.sprite.rect.x > self.rect.x:
            self.speed.x = (x_launch + random.randrange(0, self.desired_speed*0.1))
        elif self.target.sprite.rect.x < self.rect.x:
            self.flip_sprite = True
            self.speed.x = -(x_launch + random.randrange(0, self.desired_speed*0.1))
        else:
            self.speed.x = 0

        if self.target.sprite.rect.y > self.rect.y:
            self.speed.y = (y_launch + random.randrange(0, self.desired_speed*0.1))
        elif self.target.sprite.rect.y < self.rect.y:
            self.speed.y = -(y_launch + random.randrange(0, self.desired_speed*0.1))
        else:
            self.speed.y = 0

        # print(f"Launch! ({self.speed.x}, {self.speed.y})")
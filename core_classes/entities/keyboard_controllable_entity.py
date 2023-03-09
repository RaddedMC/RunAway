# Run Away
# By James Nicholls, Kelsey Kloosterman, Lukas Adie, and Sharaf Syed
# Made for SE 2250, made for life

# Imports
from core_classes.entities.moving_entity import moving_entity
import pygame as pyg
import constants_config

class keyboard_controllable_entity(moving_entity):
    def move_with_keys(self, keys, speed):

        ## Determine x direction
        x_dir = 0

        # Check left keys
        for key in constants_config.KEYS_LEFT:
            if keys[key]:
                x_dir = -1
                break
        
        # Check right keys
        if x_dir == 0:
            for key in constants_config.KEYS_RIGHT:
                if keys[key]:
                    x_dir = 1
                    break
        
        # Set x speed
        self.set_speed(x=x_dir*speed)


        ## Determine y direction
        y_dir = 0

        # Check up keys
        for key in constants_config.KEYS_UP:
            if keys[key]:
                y_dir = -1
                break
        
        # Check right keys
        if y_dir == 0:
            for key in constants_config.KEYS_DOWN:
                if keys[key]:
                    y_dir = 1
                    break
        
        # Set x/y speed
        self.set_speed(y=y_dir*speed)
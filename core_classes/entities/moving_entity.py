# Run Away
# By James Nicholls, Kelsey Kloosterman, Lukas Adie, and Sharaf Syed
# Made for SE 2250, made for life

# Imports
from core_classes.spawnable import spawnable
import pygame as pyg
import constants_config

# Used for any Spawnable that can move!
class moving_entity(spawnable):
    def __init__(self, spawn_position, sprite="res/tile/circle_player_test.png", size = {"x": 1, "y": 2}):
        spawnable.__init__(self, spawn_position, sprite, size)

        self.speed = {"x": 0, "y": 0}

    # Adds keyboard controls!
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
        
        # Check down keys
        if y_dir == 0:
            for key in constants_config.KEYS_DOWN:
                if keys[key]:
                    y_dir = 1
                    break
        
        # Set y speed
        self.set_speed(y=y_dir*speed)

    # Used above and in other areas
    def set_speed(self, x=None, y=None):
        if x == None:
            x = self.speed["x"]
        if y == None:
            y = self.speed["y"]
        self.speed = {"x": x, "y": y}

    # Move the entity! Also handle collisions.
    def update_position(self, time_scale = 0, collision_group = None):
        # This only needs to be done if the speed is nonzero
        if not self.speed["x"] == 0 or not self.speed["y"] == 0:
            # Move the rectangle
            pixels_to_move = {"x": self.speed["x"]*time_scale, "y": self.speed["y"]*time_scale}
            self.rect = self.rect.move(pixels_to_move["x"], pixels_to_move["y"])

            if not collision_group == None:
                self.collision_check(collision_group, pixels_to_move)
    
    def collision_check(self, collision_group, pixels_to_move):
        # If the moving entity collides with anything in the collision group after moving
            for spri in collision_group:
                if self.rect.colliderect(spri.rect):
                    # Cancel the move
                    self.rect = self.rect.move(-pixels_to_move["x"], -pixels_to_move["y"])

                    # Try to reduce the amount moved until the collision stops
                    collided = True
                    speedFactor = 1

                    # If still colliding
                    while collided:

                        adj_pixels = {"x": pixels_to_move["x"] - speedFactor, "y": pixels_to_move["y"] - speedFactor}
                        for key in pixels_to_move:
                            if pixels_to_move[key] < speedFactor:
                                adj_pixels[key] = 0

                        # Move by 1 less than the previous speed
                        self.rect = self.rect.move(adj_pixels["x"], adj_pixels["y"])
                        collided = self.rect.colliderect(spri.rect)
                        # If still bumping, undo move and move 1 less the next time
                        if collided:
                            self.rect = self.rect.move(-adj_pixels["x"], -adj_pixels["y"])
                            speedFactor+=1
                    break
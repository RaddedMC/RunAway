# Run Away
# By James Nicholls, Kelsey Kloosterman, Lukas Adie, and Sharaf Syed
# Made for SE 2250, made for life

# Imports
from core_classes.entities.moving_entity import moving_entity
import constants_config

# A Spawnable that can jump!
class jumpable_entity(moving_entity):
    def __init__(self, spawn_position, sprite="res/tile/circle_player_test.png", size = {"x": 1, "y": 2}, gravity = 1):
        moving_entity.__init__(self, spawn_position, sprite, size)
        self.speed = {"x": 0, "y": 0}
        self.gravity = gravity

    # Now only the horizontal speed should be externally changed
    def set_speed(self, x=None, y=None):
        if x == None:
            x = self.speed["x"]
        self.speed = {"x": x, "y": self.speed["y"]}

    def jump(self, collision_group, jump_speed, gravity = None):

        # Jumps should only be able to activate if on solid ground (by default)
        if self.is_on_ground(collision_group):
            if "jump_sound" in dir(self):
                self.jump_sound.play(0)
            self.speed = {"x": self.speed["x"], "y": -jump_speed}
            self.gravity = gravity if not gravity == None else self.gravity

    def is_on_ground(self, collision_group):
        # Move down 1 tile
        # return True if collision
        self.rect = self.rect.move(0, 1)

        for spri in collision_group:
            if self.rect.colliderect(spri.rect):
                self.rect = self.rect.move(0, -1)
                return True
        return False

    # Should be the same as the other position, but upon collision with a wall, vertical speed should be set to zero
    def update_position(self, time_scale = 0, collision_group = None):
            print(self.speed)
        # Step 1: Move!
            # Move left/right as normally
            # If on the ground, do nothing with the height (vertical speed = 0)
            if self.speed["y"] >= 0 and self.is_on_ground(collision_group):
                self.speed["y"] = 0
            # If in the air, decrease the speed by gravity
            else:
                self.speed["y"] += self.gravity

            pixels_to_move = {"x": self.speed["x"]*time_scale, "y": self.speed["y"]*time_scale}

            self.rect = self.rect.move(pixels_to_move["x"], pixels_to_move["y"])

        # Step 2: Collision check
            # Same as in moving_entity
            if not collision_group == None:
                self.collision_check(collision_group, pixels_to_move)

    # Adds keyboard controls. This time all we want is x direction and jump
    def move_with_keys(self, keys, speed, collision_group, jump_speed=0.5, gravity = None):

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

        # Check up keys for jump
        for key in constants_config.KEYS_UP:
            if keys[key]:
                self.jump(collision_group=collision_group, gravity=gravity, jump_speed=jump_speed)
                break
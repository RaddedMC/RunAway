# Run Away
# By James Nicholls, Kelsey Kloosterman, Lukas Adie, and Sharaf Syed
# Made for SE 2250, made for life

# Imports
import pygame as pyg
from core_classes.world.level import level
from core_classes.entities.keyboard_controllable_entity import keyboard_controllable_entity
from time import sleep as zzz

# This method starts the game.
def init():
    pyg.init()

    # Initialize level
    lvl_test = level()

    # Initialize player
    player = keyboard_controllable_entity(spawn_position={"x": 2, "y": 2})
    
    # Separate Surfaces allows for the game to run at any (16:9) resolution at fullscreen and scale properly.
    sys_screen = pyg.display.set_mode((256*3,144*3))
    game_screen = pyg.Surface((256,144))

    # The main game loop! Isolated in a function for better encapuslation
    def main_loop():
        running = True
        while running:
            # Event loop
            for ev in pyg.event.get():

                # Exit the game on quit attempt
                if ev.type == pyg.QUIT:
                    running = False

            # Redraw level background
            game_screen.blit(lvl_test.background, (0,0))

            # Handle player movement
            keys = pyg.key.get_pressed()
            player.move_with_keys(keys, 5)
            player.update_position(1)

            # Draw level blocks and player to game screen
            lvl_test.blocks.draw(game_screen)
            game_screen.blit(player.image, player.rect)

            # Upscale the game Surface and display to the user's screen
            scaled_game_disp = pyg.transform.scale(game_screen, (sys_screen.get_width(), sys_screen.get_height()))
            sys_screen.blit(scaled_game_disp, (0,0))
            pyg.display.flip()


            # Sleep and repeat
            zzz(0.01)
    
    main_loop()

    pyg.quit()


if __name__ == "__main__":
    init()
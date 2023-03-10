# Run Away
# By James Nicholls, Kelsey Kloosterman, Lukas Adie, and Sharaf Syed
# Made for SE 2250, made for life

# Imports
import pygame as pyg
from core_classes.world.level import level
from core_classes.entities.moving_entity import moving_entity
from core_classes.entities.jumpable_entity import jumpable_entity
from constants_config import FPS
from constants_config import KEYS_QUIT
from time import sleep as zzz

# This method starts the game.
def init():
    pyg.init()

    # Initialize level
    lvl_test = level()

    # Initialize player
    player = jumpable_entity(spawn_position={"x": 2, "y": 2}, gravity=0.01)
    player.jump_sound = pyg.mixer.Sound("res/aud/jump_test.wav")
    
    # Separate Surfaces allows for the game to run at any (16:9) resolution at fullscreen and scale properly.
    sys_screen = pyg.display.set_mode((0,0), pyg.FULLSCREEN)
    game_screen = pyg.Surface((256,144))

    # The main game loop! Isolated in a function for better encapuslation
    clock = pyg.time.Clock() # for frame-independent movement
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

            for key in KEYS_QUIT:
                if keys[key]:
                    running = False

            player.move_with_keys(keys, 0.2, collision_group=lvl_test.blocks) # Keep this between 0.2 and 0.5 for EVERYTHING
            player.update_position(clock.tick(FPS), collision_group=lvl_test.blocks)

            # Draw level blocks and player to game screen
            lvl_test.blocks.draw(game_screen)
            game_screen.blit(player.image, player.rect)

            # Upscale the game Surface and display to the user's screen
            scaled_game_disp = pyg.transform.scale(game_screen, (sys_screen.get_width(), sys_screen.get_height()))
            sys_screen.blit(scaled_game_disp, (0,0))
            pyg.display.flip()
    
    # This way if the game crashes (and the exception makes it out of the main loop), the game will stop immediately
    import traceback
    try:
        main_loop()
    except:
        print(traceback.format_exc())

    pyg.quit()


if __name__ == "__main__":
    init()
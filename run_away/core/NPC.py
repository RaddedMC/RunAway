from core.entity import AnimatedEntity, InteractableEntity
import pygame
import config
from utils.tools import get_sounds_by_key
import random


class NPC(InteractableEntity):
    def __init__(self,
                 groups: pygame.sprite.Group, 
                 collidable_sprites: pygame.sprite.Group, 
                 pos: tuple, 
                 root_dir: str, 
                 dialogue: list,                 
                 speed: float = 0, 
                 gravity: float = 0,
                 ):
        
        self.pos = pos        
        self.dialogue = dialogue
        super().__init__(groups, collidable_sprites, pos, root_dir, speed, gravity)
        self.msg_index = 0
        self.message = config.GAME_FONT.render(f"{self.dialogue[self.msg_index]}", True, (255, 255, 255))
        self.message_rect = self.message.get_rect(topleft = (self.pos[0], self.pos[1]))
        

    def interact(self):
        self.message = config.GAME_FONT.render(f"{self.dialogue[self.msg_index]}", True, (255, 255, 255))
        display_surface = pygame.display.get_surface()
        display_surface.blit(self.message, self.message_rect)
        self.msg_index += 1
        self.msg_index = self.msg_index % len(self.dialogue)


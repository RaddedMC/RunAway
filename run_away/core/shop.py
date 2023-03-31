from core.entity import Block
import pygame
import config
from utils.tools import get_sounds_by_key
import random
from pytmx.util_pygame import load_pygame
from pathlib import Path

class Shop():

    def __init__(self, rect: pygame.rect.Rect, stats: dict, inShop:bool):
        
        self.inShop = inShop
        self.rect = rect

        self.healthUp = pygame.rect.Rect()
        self.healthDown = pygame.rect.Rect()
        self.strUp = pygame.rect.Rect()
        self.agUp = pygame.rect.Rect()
        self.agDown = pygame.rect.Rect()
        self.agUp = pygame.rect.Rect()

        self.background = pygame.sprite.Group()
        self.stats = stats
        import_assets()



    def import_assets(self):
        tmx_data = load_pygame(Path("run_away/resources/gfx/GUI/shop.tmx"))

        for layer in tmx_data.get_visible_layers():
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    Block(self.background, (x, y), surf)
        
        for obj in tmx_data.get_layer_by_name("StatNumbers"):
            if hasattr(obj, "text"):
                obj.text = self.stats[obj.name.lower()]

            elif obj.name == "Increase_Health":
                self.healthUp = pygame.rect.Rect(obj.x, obj.y, obj.width, obj.height)
            elif obj.name == "Decrease_Health":
                self.healthDown = pygame.rect.Rect(obj.x, obj.y, obj.width, obj.height)
            elif obj.name == "Increase_Strength":
                self.strUp = pygame.rect.Rect(obj.x, obj.y, obj.width, obj.height)
            elif obj.name == "Decrease_Strength":
                self.strDown = pygame.rect.Rect(obj.x, obj.y, obj.width, obj.height)
            elif obj.name == "Increase_Agility":
                self.agUp = pygame.rect.Rect(obj.x, obj.y, obj.width, obj.height)
            elif obj.name == "Decrease_Agility":
                self.agDown = pygame.rect.Rect(obj.x, obj.y, obj.width, obj.height)
            


                    

    def interact():

        display_surface = pygame.get
        pass


    # get boolean to hijack run() method of Level, iterate through each visible layer as sprites with their rectangles
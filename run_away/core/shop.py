from core.entity import Block
import pygame
from pygame import Rect
import config
from utils.tools import get_sounds_by_key
import random
from pytmx.util_pygame import load_pygame
from pathlib import Path

class Shop():

    def __init__(self, rect: pygame.rect.Rect, stats: dict, inShop:bool):
        
        self.inShop = inShop
        self.rect = rect

        self.healthUp: Rect
        self.healthDown: Rect
        self.strUp: Rect
        self.agUp: Rect
        self.agDown: Rect
        self.agUp: Rect

        self.close: Rect

        self.background = pygame.sprite.Group()
        self.stats = stats
        self.import_assets()



    def import_assets(self):
        tmx_data = load_pygame(Path("run_away/resources/gfx/GUI/shop.tmx"))

        for layer in tmx_data.visible_layers:
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    Block(self.background,
                          (x * config.TILE_SIZE, y * config.TILE_SIZE), 
                          surf,
                          )
        
        for obj in tmx_data.get_layer_by_name("StatNumbers"):
            if hasattr(obj, "text"):
                pass

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
            elif obj.name == "close":
                self.close = pygame.rect.Rect(obj.x, obj.y, obj.width, obj.height)
            



    def interact(self):
        # print("Shop Loaded!")
        display_surface = pygame.display.get_surface()
        self.background.draw(display_surface)

        click = False
        (mx, my) = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.inShop = False
                    print(self.inShop)


        if (self.stats["coins"] >= 7):
            pass
        else:
            if self.healthUp.collidepoint(mx, my) and click == True:
                self.stats["health"] += 1
                coins -= config.SHOP_DATA["price"]
            if self.healthDown.collidepoint(mx, my) and click == True:
                self.stats["health"] += 1
                coins -= config.SHOP_DATA["price"]
            if self.strUp.collidepoint(mx, my) and click == True:
                self.stats["health"] += 1
                coins -= config.SHOP_DATA["price"]
            if self.strDown.collidepoint(mx, my) and click == True:
                self.stats["health"] += 1
                coins -= config.SHOP_DATA["price"]
            if self.agUp.collidepoint(mx, my) and click == True:
                self.stats["health"] += 1
                coins -= config.SHOP_DATA["price"]
            if self.agDown.collidepoint(mx, my) and click == True:
                self.stats["health"] += 1
                coins -= config.SHOP_DATA["price"]
        
        return self.inShop
            
        


    # get boolean to hijack run() method of Level, iterate through each visible layer as sprites with their rectangles
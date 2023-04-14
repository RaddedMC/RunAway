import pygame
from pygame import Rect
from pytmx.util_pygame import load_pygame

from run_away import config
from run_away.core.entity import Block


class Shop:
    def __init__(
        self, rect: pygame.rect.Rect, render_surface: pygame.Surface, stats: dict
    ):
        self.inShop = False
        self.rect = rect

        self.healthUp: Rect
        self.healthDown: Rect
        self.strUp: Rect
        self.agUp: Rect
        self.agDown: Rect
        self.agUp: Rect

        self.health = stats["health"]
        self.health_rect: Rect

        self.strength = stats["strength"]
        self.strength_rect: Rect

        self.agility = stats["agility"]
        self.agility_rect: Rect

        self.coins = stats["coins"]
        self.coins_rect: Rect

        self.render_surface = render_surface
        self.display_surface = pygame.display.get_surface()
        self.close: Rect

        self.background = pygame.sprite.Group()
        self.stats = stats
        self.import_assets()

    def import_assets(self):
        tmx_data = load_pygame(config.GFX_PATH.joinpath("GUI", "shop.tmx"))

        for layer in tmx_data.visible_layers:
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    Block(
                        self.background,
                        (x * config.TILE_SIZE, y * config.TILE_SIZE),
                        surf,
                    )

        for obj in tmx_data.get_layer_by_name("StatNumbers"):
            if obj.name == "Health":
                self.health = config.MENU_FONT.render(
                    f"{self.stats[obj.name.lower()]}", True, (0, 0, 0)
                )
                self.health_rect = self.health.get_rect(
                    center=(obj.x + obj.width / 2, obj.y + obj.height / 2)
                )
            if obj.name == "Strength":
                self.strength = config.MENU_FONT.render(
                    f"{self.stats[obj.name.lower()]}", True, (0, 0, 0)
                )
                self.strength_rect = self.health.get_rect(
                    center=(obj.x + obj.width / 2, obj.y + obj.height / 2)
                )
            if obj.name == "Agility":
                self.agility = config.MENU_FONT.render(
                    f"{self.stats[obj.name.lower()]}", True, (0, 0, 0)
                )
                self.agility_rect = self.health.get_rect(
                    center=(obj.x + obj.width / 2, obj.y + obj.height / 2)
                )
            if obj.name == "Coins":
                self.coins = config.MENU_FONT.render(
                    f"{self.stats[obj.name.lower()]}", True, (0, 0, 0)
                )
                self.coins_rect = self.health.get_rect(
                    center=(obj.x + obj.width / 2, obj.y + obj.height / 2)
                )

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
        self.inShop = True
        # print("Shop Loaded!")
        self.render_surface.fill("black")
        self.background.draw(self.render_surface)

        coin_color = 0
        if self.stats["coins"] < 7:
            coin_color = 255
        else:
            coin_color = 0

        self.health = config.MENU_FONT.render(
            f"{self.stats['health']}", True, (0, 0, 0)
        )
        self.strength = config.MENU_FONT.render(
            f"{self.stats['strength']}", True, (0, 0, 0)
        )
        self.agility = config.MENU_FONT.render(
            f"{self.stats['agility']}", True, (0, 0, 0)
        )

        self.coins = config.MENU_FONT.render(
            f"{self.stats['coins']}", True, (coin_color, 0, 0)
        )

        self.render_surface.blit(self.health, self.health_rect)
        self.render_surface.blit(self.strength, self.strength_rect)
        self.render_surface.blit(self.agility, self.agility_rect)
        self.render_surface.blit(self.coins, self.coins_rect)

        scaled_display = pygame.transform.scale(
            self.render_surface,
            (self.display_surface.get_width(), self.display_surface.get_height()),
        )

        self.display_surface.blit(scaled_display, (0, 0))

        click = False
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = list(mouse_pos)
        mouse_pos[0] = (
            mouse_pos[0]
            * self.render_surface.get_width()
            / self.display_surface.get_width()
        )
        mouse_pos[1] = (
            mouse_pos[1]
            * self.render_surface.get_width()
            / self.display_surface.get_width()
        )

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if self.close.collidepoint(mouse_pos) and click is True:
            self.inShop = False

        if (
            self.healthUp.collidepoint(mouse_pos)
            and click is True
            and self.stats["coins"] >= 7
        ):
            self.stats["health"] += 1
            self.stats["coins"] -= config.SHOP_DATA["price"]

        if self.healthDown.collidepoint(mouse_pos) and click is True:
            if self.stats["health"] > 10:
                self.stats["health"] -= 1
                self.stats["coins"] += config.SHOP_DATA["price"]

        if (
            self.strUp.collidepoint(mouse_pos)
            and click is True
            and self.stats["coins"] >= 7
        ):
            self.stats["strength"] += 1
            self.stats["coins"] -= config.SHOP_DATA["price"]
        if self.strDown.collidepoint(mouse_pos) and click is True:
            if self.stats["strength"] > 10:
                self.stats["strength"] -= 1
                self.stats["coins"] += config.SHOP_DATA["price"]

        if (
            self.agUp.collidepoint(mouse_pos)
            and click is True
            and self.stats["coins"] >= 7
        ):
            self.stats["agility"] += 1
            self.stats["coins"] -= config.SHOP_DATA["price"]

        if self.agDown.collidepoint(mouse_pos) and click is True:
            if self.stats["agility"] > 10:
                self.stats["agility"] -= 1
                self.stats["coins"] += config.SHOP_DATA["price"]

        return self.inShop

    # get boolean to hijack run() method of Level, iterate through each visible layer as sprites with their rectangles

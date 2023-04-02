import pygame

from core.entity import Entity

class Weapon(Entity):
    def __init__(self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple,
        image: pygame.Surface,
        damage: int
        ):
        super().__init__(groups, collidable_sprites, pos, pygame.image.load(image))
        self.damage = damage

    def destroy(self):
        self.image.fill((0,0,0,0))
        del self

    def stopDamage(self):
        self.damage=0
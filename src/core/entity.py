import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, image, speed, groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.speed = speed

    def update(self, dt: float):
        self.move()
        self.collision()

    def move(self, dt: float):
        pass

    def collision(self):
        pass

class AnimatedEntity(Entity):
    def __init__(self, pos, animation_data, groups):
        super().__init__(groups)
        # self.frames = import_folder(animation_data["frames"]) # or similar name
        # self.frame_index = 0
        # self.animate_speed = animation_data["speed"]
        # self.image = self.frames[self.frame_index]

    def animate(self):
        pass

    def update(self, dt: float):
        self.move()
        self.collision()
        self.animate()

class InteractableEntity(Entity):
    def __init__(self, pos, image, speed, name, groups):
        super().__init__(pos, image, speed, groups)
        self.name = name

class Portal(InteractableEntity):
    pass

class NPC(InteractableEntity):
    pass


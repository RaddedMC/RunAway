from core.entity import AnimatedEntity
import pygame

class Home(AnimatedEntity):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collitable_sprites: pygame.sprite.Group,
        pos: tuple
    ):
        super().__init__(
            groups=groups,
            collidable_sprites=collitable_sprites,
            pos=pos,
            root_dir="./run_away/resources/gfx/objects/home/",
            speed=0,
            gravity=0
        )
        self.animation_speed = 0

    def set_frame_by_percent(self, per):
        # FIXME: this number keeps jumping to something random and strange
        potential_frame = round(per*9)
        if not round(per*9) > 9 and not potential_frame < 0:
            self.index_i_want = potential_frame

    def animate(self, dt: float):
        if not hasattr(self,"index_i_want"):
            self.index_i_want = 0

        animation = self.animations[self.status]

        # Set the image for the current frame
        print(self.index_i_want)
        image_path = animation[self.index_i_want]
        self.image = pygame.image.load(image_path)
        if self.flip_sprite:
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
        self.rect = self.image.get_rect(center=self.rect.center)
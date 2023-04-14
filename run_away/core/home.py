from pathlib import Path
from typing import Union

import pygame

from run_away.core.entity import AnimatedEntity


class Home(AnimatedEntity):
    def __init__(
        self,
        groups: pygame.sprite.Group,
        collidable_sprites: pygame.sprite.Group,
        pos: tuple[int, int],
        root_dir: Union[str, Path],
    ) -> None:
        super().__init__(
            groups=groups,
            collidable_sprites=collidable_sprites,
            pos=pos,
            root_dir=root_dir,
            animation_speed=0,
            speed=0,
            gravity=0,
        )

    def set_frame_by_percent(self, per: float) -> None:
        # FIXME: this number keeps jumping to something random and strange
        potential_frame = round(per * 9)
        if not round(per * 9) > 9 and not potential_frame < 0:
            self.index_i_want = potential_frame

    def animate(self, dt: float) -> None:
        if not hasattr(self, "index_i_want"):
            self.index_i_want = 0

        animation = self.animations[self.status]

        # Set the image for the current frame
        image_path = animation[self.index_i_want]
        self.image = pygame.image.load(image_path)
        if self.flip_sprite:
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
        self.rect = self.image.get_rect(center=self.rect.center)

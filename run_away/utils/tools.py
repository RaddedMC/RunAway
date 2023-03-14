# Contains common operations used by multiple classes

import pprint
from pathlib import Path


def import_folder():
    pass


def import_animations(folder_path: str):
    animations = {}

    for path in Path(folder_path).iterdir():
        if path.is_dir():
            animations.update({f"{path.name}": [child for child in path.iterdir()]})

    return animations


if __name__ == "__main__":  # DEBUG
    pprint.pprint(import_animations(Path("./resources/gfx/player/")))

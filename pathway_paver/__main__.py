"""Allows running the game with ``python -m pathway_paver``."""

import pygame

from . import scenes
from .game import play_level
from .screens import main_menu, level_selection_screen

SCENE_HANDLERS = {
    scenes.MAIN_MENU: main_menu,
    scenes.LEVEL_SELECT: level_selection_screen,
    scenes.PLAY: play_level,
}


def main():
    scene = scenes.MAIN_MENU
    while scene != scenes.QUIT:
        scene = SCENE_HANDLERS[scene]()
    pygame.quit()


if __name__ == "__main__":
    main()

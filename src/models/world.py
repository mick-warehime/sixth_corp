from models.theme_base import Theme
from models.themes import CityTheme


class World(object):
    def __init__(self) -> None:
        self.theme: Theme = CityTheme()


_world = None


def get_world() -> World:
    global _world
    if _world is None:
        reset_world()
    return _world


def reset_world() -> None:
    global _world
    _world = World()


def get_theme() -> Theme:
    return get_world().theme

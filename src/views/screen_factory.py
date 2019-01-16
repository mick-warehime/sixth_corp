from views.pygame_screen import PygameScreen
from views.screen_base import Screen

_screen = None


def get_screen() -> Screen:
    global _screen
    if _screen is None:
        _screen = PygameScreen()
    return _screen

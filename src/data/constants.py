from enum import Enum

FRAMES_PER_SECOND = 30
LOG_LEVEL = 'DEBUG'
LOGGING_FILE = 'src/logging/game.log'
PREFERENCES_FILE = 'src/data/bindings.pref'
SCREEN_SIZE = (1600, 1200)
TEXTWIDTH = 68
VERSION = 0.001


class BackgroundImages(Enum):
    LOADING = 'src/data/images/background_loading.png'
    CITY = 'src/data/images/background_city.png'
    MARS = 'src/data/images/background_mars.png'
    SETTINGS = 'src/data/images/background_settings.png'
    INVENTORY = 'src/data/images/background_inventory.png'

    @property
    def path(self) -> str:
        return self.value

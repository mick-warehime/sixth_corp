from models.characters.character_base import Character
from models.characters.character_examples import CharacterTypes
from models.characters.character_impl import build_character
from models.world.location_base import Location

_BACKGROUND_IMAGE_LOADING = 'src/data/images/background_loading.png'
_BACKGROUND_IMAGE_CITY = 'src/data/images/background_city.png'
_BACKGROUND_IMAGE_MARS = 'src/data/images/background_mars.png'


class LoadingLocation(Location):

    def __init__(self) -> None:
        super().__init__(_BACKGROUND_IMAGE_LOADING)

    def random_enemy(self) -> Character:
        raise NotImplementedError('LoadingLocation should not give enemies.')


class MarsLocation(Location):

    def __init__(self) -> None:
        super().__init__(_BACKGROUND_IMAGE_MARS)

    def random_enemy(self) -> Character:
        return build_character(CharacterTypes.DRONE.data)


class CityLocation(Location):

    def __init__(self) -> None:
        super().__init__(_BACKGROUND_IMAGE_CITY)

    def random_enemy(self) -> Character:
        return build_character(CharacterTypes.DRONE.data)

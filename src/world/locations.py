from characters.character_base import Character
from characters.character_factory import CharacterTypes, build_character
from world.location_base import Location

_BACKGROUND_IMAGE_LOADING = 'src/images/background_loading.png'
_BACKGROUND_IMAGE_CITY = 'src/images/background_city.png'
_BACKGROUND_IMAGE_MARS = 'src/images/background_mars.png'


class LoadingLocation(Location):

    def __init__(self) -> None:
        super().__init__(_BACKGROUND_IMAGE_LOADING)

    # TODO - this doesnt make sense here
    def random_enemy(self) -> Character:
        return build_character(CharacterTypes.DRONE)


class MarsLocation(Location):

    def __init__(self) -> None:
        super().__init__(_BACKGROUND_IMAGE_MARS)

    def random_enemy(self) -> Character:
        return build_character(CharacterTypes.DRONE)


class CityLocation(Location):

    def __init__(self) -> None:
        super().__init__(_BACKGROUND_IMAGE_CITY)

    def random_enemy(self) -> Character:
        return build_character(CharacterTypes.DRONE)

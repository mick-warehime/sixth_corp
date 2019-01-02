from world.location_base import Location

_BACKGROUND_IMAGE_LOADING = 'src/images/background_loading.png'
_BACKGROUND_IMAGE_CITY = 'src/images/background_city.png'
_BACKGROUND_IMAGE_MARS = 'src/images/background_mars.png'


class LoadingLocation(Location):

    def __init__(self) -> None:
        super().__init__(_BACKGROUND_IMAGE_LOADING)


class MarsLocation(Location):

    def __init__(self) -> None:
        super().__init__(_BACKGROUND_IMAGE_MARS)


class CityLocation(Location):

    def __init__(self) -> None:
        super().__init__(_BACKGROUND_IMAGE_CITY)

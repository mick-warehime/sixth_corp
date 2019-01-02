from world.location_base import Location

BACKGROUND_IMAGE_LOADING = 'src/images/background_loading.png'
BACKGROUND_IMAGE_CITY = 'src/images/background_city.png'


class MarsLocation(Location):

    def __init__(self) -> None:
        super().__init__(BACKGROUND_IMAGE_LOADING)


class CityLocation(Location):

    def __init__(self) -> None:
        super().__init__(BACKGROUND_IMAGE_CITY)

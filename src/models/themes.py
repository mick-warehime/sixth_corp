from models.theme_base import Theme

BACKGROUND_IMAGE_LOADING = 'src/images/background_loading.png'
BACKGROUND_IMAGE_CITY = 'src/images/background_city.png'


class LoadingTheme(Theme):

    def __init__(self) -> None:
        super().__init__(BACKGROUND_IMAGE_LOADING)


class CityTheme(Theme):

    def __init__(self) -> None:
        super().__init__(BACKGROUND_IMAGE_CITY)

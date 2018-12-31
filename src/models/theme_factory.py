from typing import Optional
from models.theme_base import Theme
from models.themes import LoadingTheme
from models.themes import CityTheme


def next_theme(prev_theme: Optional[Theme]) -> Theme:
    if prev_theme is None:
        return LoadingTheme()
    elif isinstance(prev_theme, LoadingTheme):
        return CityTheme()
    else:
        raise NotImplementedError('No theme after city')
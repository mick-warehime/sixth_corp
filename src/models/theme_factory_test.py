from unittest import TestCase
from models.theme_factory import next_theme
from models.themes import LoadingTheme, CityTheme


class ThemeFactoryTest(TestCase):

    def test_first_theme_loading(self):
        first_theme = next_theme(None)
        self.assertIsInstance(first_theme, LoadingTheme)

    def test_second_theme_city(self):
        first_theme = next_theme(None)
        second_theme = next_theme(first_theme)
        self.assertIsInstance(second_theme, CityTheme)

    def test_no_third_theme(self):
        first_theme = next_theme(None)
        second_theme = next_theme(first_theme)
        with self.assertRaises(NotImplementedError):
            next_theme(second_theme)

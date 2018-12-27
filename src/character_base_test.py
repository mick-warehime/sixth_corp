from character_base import Character
from unittest import TestCase

from conditions import IsDead
from states import Attribute


class CharacterTest(TestCase):

    def test_character_has_attributes(self):
        health = 10
        char = Character(health)
        assert char.get_attribute(Attribute.HEALTH)

    def test_kill_character(self):
        health = 10
        char = Character(health)
        char.increment_attribute(Attribute.HEALTH, -health)
        self.assertTrue(IsDead().check(char))

from character_base import Character
from character_state import State
from unittest import TestCase


class CharacterTest(TestCase):

    def test_character_has_attributes(self):
        health = 10
        char = Character(health)
        self.assertTrue(char.has_state(State.HEALTH))

    def test_kill_character(self):
        health = 10
        char = Character(health)
        char.update_state(State.HEALTH, -health)
        self.assertFalse(char.is_alive())

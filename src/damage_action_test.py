from character_base import Character
from damage_action import DamageAction
from parameterized import parameterized
from unittest import TestCase

from states import Attribute


class DamageActionTest(TestCase):

    @parameterized.expand([[-10], [0]])
    def test_damage_negative_raises(self, damage):
        with self.assertRaises(ValueError):
            DamageAction(damage)

    def test_damage_applies_correctly(self):
        character_health = 20
        char = Character(character_health)
        ten_damage = DamageAction(10)

        ten_damage.apply(char)

        self.assertEqual(char.get_attribute(Attribute.HEALTH),
                         character_health - 10)

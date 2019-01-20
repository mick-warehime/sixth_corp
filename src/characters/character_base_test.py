from unittest import TestCase

from characters.ability_examples import FireLaser
from characters.character_examples import CharacterData
from characters.character_factory import build_character
from characters.chassis_examples import ChassisData
from characters.conditions import IsDead
from characters.mods_base import GenericMod, Slots
from characters.states import Attribute, State


class CharacterTest(TestCase):

    def _character(self):
        chassis = ChassisData({Slots.STORAGE: 10},
                              attribute_modifiers={Attribute.MAX_HEALTH: 10})
        return build_character(CharacterData(chassis))

    def test_character_has_attributes(self):
        char = self._character()
        assert char.get_attribute(Attribute.HEALTH)

    def test_kill_character(self):
        char = self._character()
        health = char.get_attribute(Attribute.HEALTH)
        char.increment_attribute(Attribute.HEALTH, -health)
        self.assertTrue(IsDead().check(char))

    def test_character_state_change(self):
        char = self._character()

        assert not char.has_state(State.ON_FIRE)
        char.attempt_pickup(GenericMod(states_granted=State.ON_FIRE))
        assert char.has_state(State.ON_FIRE)

    def test_mods_affect_max_attribute(self):
        char = self._character()
        max_health = char.get_attribute(Attribute.MAX_HEALTH)
        bonus = 5
        char.attempt_pickup(
            GenericMod(attribute_modifiers={Attribute.MAX_HEALTH: bonus}))

        assert char.get_attribute(Attribute.MAX_HEALTH) == max_health + bonus

    def test_max_attributes_determine_bounds(self):
        char = self._character()
        max_health = char.get_attribute(Attribute.MAX_HEALTH)
        bonus = 5

        assert char.get_attribute(Attribute.HEALTH) == max_health
        char.increment_attribute(Attribute.HEALTH, bonus)
        assert char.get_attribute(Attribute.HEALTH) == max_health

    def test_mods_add_abilities(self):
        char = self._character()

        ability = FireLaser(12)
        assert ability not in char.abilities()

        char.attempt_pickup(GenericMod(abilities_granted=ability))
        assert ability in char.abilities()

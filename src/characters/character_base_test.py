from unittest import TestCase

from characters.ability_examples import FireLaser
from characters.character_impl import CharacterImpl
from characters.chassis_examples import ChassisTypes
from characters.conditions import IsDead
from characters.mod_examples import HelmOfBeingOnFire, HullPlating
from characters.mods_base import GenericMod
from characters.states import Attribute, State


class CharacterTest(TestCase):

    def test_character_has_attributes(self):
        char = CharacterImpl()
        assert char.get_attribute(Attribute.HEALTH)

    def test_kill_character(self):
        char = CharacterImpl()
        health = char.get_attribute(Attribute.HEALTH)
        char.increment_attribute(Attribute.HEALTH, -health)
        self.assertTrue(IsDead().check(char))

    def test_character_state_change(self):
        char = CharacterImpl()

        assert not char.has_state(State.ON_FIRE)
        char.attempt_pickup(HelmOfBeingOnFire())
        assert char.has_state(State.ON_FIRE)

    def test_mods_affect_max_attribute(self):
        char = CharacterImpl()
        max_health = char.get_attribute(Attribute.MAX_HEALTH)
        bonus = 5
        char.attempt_pickup(HullPlating(bonus))

        assert char.get_attribute(Attribute.MAX_HEALTH) == max_health + bonus

    def test_max_attributes_determine_bounds(self):
        char = CharacterImpl()
        max_health = char.get_attribute(Attribute.MAX_HEALTH)
        bonus = 5

        assert char.get_attribute(Attribute.HEALTH) == max_health
        char.increment_attribute(Attribute.HEALTH, bonus)
        assert char.get_attribute(Attribute.HEALTH) == max_health

    def test_mods_add_abilities(self):
        char = CharacterImpl()

        ability = FireLaser(12)
        assert ability not in char.abilities()

        char.attempt_pickup(GenericMod(abilities_granted=ability))
        assert ability in char.abilities()

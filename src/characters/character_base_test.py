from unittest import TestCase

from characters.ability_examples import FireLaser
from characters.character_impl import CharacterImpl
from characters.conditions import IsDead
from characters.mod_examples import HelmOfBeingOnFire, HullPlating
from characters.mods_base import GenericMod
from characters.states import Attribute, State


class CharacterTest(TestCase):

    def test_character_has_attributes(self):
        health = 10
        char = CharacterImpl(health)
        assert char.get_attribute(Attribute.HEALTH) == health

    def test_kill_character(self):
        health = 10
        char = CharacterImpl(health)
        char.increment_attribute(Attribute.HEALTH, -health)
        self.assertTrue(IsDead().check(char))

    def test_character_state_change(self):
        char = CharacterImpl(health=10)

        assert not char.has_state(State.ON_FIRE)
        char.attempt_pickup(HelmOfBeingOnFire())
        assert char.has_state(State.ON_FIRE)

    def test_mods_affect_max_attribute(self):
        health = 10
        char = CharacterImpl(health)
        max_health = char.get_attribute(Attribute.MAX_HEALTH)
        bonus = 5
        char.attempt_pickup(HullPlating(bonus))

        assert char.get_attribute(Attribute.MAX_HEALTH) == max_health + bonus

    def test_mods_add_abilities(self):
        char = CharacterImpl(10)

        assert not char.abilities()
        ability = FireLaser(4)
        char.attempt_pickup(GenericMod(abilities_granted=ability))
        assert tuple(char.abilities()) == (ability,)

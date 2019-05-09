from unittest import TestCase

from models.characters.character_examples import CharacterData
from models.characters.character_impl import build_character
from models.characters.chassis import ChassisData
from models.characters.conditions import is_dead
from models.characters.mods_base import SlotTypes, build_mod
from models.characters.states import Attributes, State
from models.characters.subroutine_examples import direct_damage

_ACTIVE_SLOT = SlotTypes.ARMS


class CharacterTest(TestCase):

    def _character(self):
        chassis = ChassisData({SlotTypes.STORAGE: 10, _ACTIVE_SLOT: 10},
                              attribute_modifiers={Attributes.MAX_HEALTH: 10})
        return build_character(data=CharacterData(chassis))

    def test_character_has_attributes(self):
        char = self._character()
        assert char.status.get_attribute(Attributes.HEALTH)

    def test_kill_character(self):
        char = self._character()
        health = char.status.get_attribute(Attributes.HEALTH)
        char.status.increment_attribute(Attributes.HEALTH, -health)
        self.assertTrue(is_dead(char))

    def test_character_state_change(self):
        char = self._character()

        assert not char.status.has_state(State.ON_FIRE)
        char.chassis.attempt_store(
            build_mod(states_granted=State.ON_FIRE, valid_slots=_ACTIVE_SLOT))
        assert char.status.has_state(State.ON_FIRE)

    def test_mods_affect_max_attribute(self):
        char = self._character()
        max_health = char.status.get_attribute(Attributes.MAX_HEALTH)
        bonus = 5
        char.chassis.attempt_store(
            build_mod(attribute_modifiers={Attributes.MAX_HEALTH: bonus},
                      valid_slots=_ACTIVE_SLOT))

        assert char.status.get_attribute(
            Attributes.MAX_HEALTH) == max_health + bonus

    def test_max_attributes_determine_bounds(self):
        char = self._character()
        max_health = char.status.get_attribute(Attributes.MAX_HEALTH)
        bonus = 5

        assert char.status.get_attribute(Attributes.HEALTH) == max_health
        char.status.increment_attribute(Attributes.HEALTH, bonus)
        assert char.status.get_attribute(Attributes.HEALTH) == max_health

    def test_mods_add_subroutines(self):
        char = self._character()

        subroutine = direct_damage(12)
        assert subroutine not in char.chassis.all_subroutines()

        char.chassis.attempt_store(
            build_mod(subroutines_granted=subroutine,
                      valid_slots=_ACTIVE_SLOT))
        assert subroutine in char.chassis.all_subroutines()

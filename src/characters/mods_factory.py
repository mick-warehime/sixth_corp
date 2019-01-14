from typing import Dict, NamedTuple, Tuple

from characters.abilities_base import Ability
from characters.mods_base import GenericMod
from characters.states import AttributeType, State

ModData = NamedTuple(
    'ModData', [('states_granted', Tuple[State, ...]),
                ('attribute_modifiers', Dict[AttributeType, int]),
                ('abilities_granted', Tuple[Ability, ...])])

ModData.__new__.__defaults__ = ((), {}, ())  # type: ignore


def build_mod(mod_data: ModData) -> GenericMod:
    return GenericMod(mod_data.states_granted, mod_data.attribute_modifiers,
                      mod_data.abilities_granted)

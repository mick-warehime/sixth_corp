from enum import Enum
from typing import Any, Dict

from characters.character_base import Character
from characters.character_examples import (DRONE, HARMLESS, HUMAN_PLAYER,
                                           USLESS, CharacterData)
from characters.enemy_base import Enemy
from characters.mods_base import GenericMod
from characters.states import Attribute
from combat.ai.ai_factory import build_ai


class CharacterFactory(Enum):
    HUMAN_PLAYER = 'human player'
    DRONE = 'drone'
    HARMLESS = 'harmless'
    USELESS = 'useless'

    def build(self) -> Character:
        data = _char_type_to_data[self]

        # We will need to refactor this. We should probably merge Character and
        # Enemy.
        character_cls: Any = Character
        if self == CharacterFactory.HUMAN_PLAYER:
            pos = 200, 500, 150, 150
        else:
            character_cls = Enemy
            pos = 800, 300, 200, 150

        # This is an intermediate fix as in future these things will be handled
        # by the chassis.
        chassis = data.chassis_type.build()
        max_health = chassis.total_modifier(Attribute.MAX_HEALTH)

        char = character_cls(health=max_health,
                             image_path=data.image_path,
                             name=data.name)

        temp_mod = GenericMod(abilities_granted=chassis.all_abilities())
        char.attempt_pickup(temp_mod)

        # TODO(mick) - move positions to combat view
        char.set_position(*pos)
        char.ai = build_ai(char, data.ai_type)  # type: ignore

        # TODO(dvirk) - set chassis for character

        return char


_char_type_to_data: Dict[CharacterFactory, CharacterData] = {
    CharacterFactory.DRONE: DRONE,
    CharacterFactory.HARMLESS: HARMLESS,
    CharacterFactory.USELESS: USLESS,
    CharacterFactory.HUMAN_PLAYER: HUMAN_PLAYER

}

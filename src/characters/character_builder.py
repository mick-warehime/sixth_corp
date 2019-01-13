from abc import abstractmethod
from enum import Enum
from typing import Any, Dict, Sequence

from characters.character_base import Character
from characters.character_examples import (DRONE, HARMLESS, HUMAN_PLAYER,
                                           USLESS, CharacterData)
from characters.chassis import Chassis
from characters.enemy_base import Enemy
from characters.mods_base import GenericMod, Mod
from characters.states import Attribute
from combat.ai.ai_factory import build_ai


class CharacterBuilder(object):
    """Abstract class used to simplify enumerating players and enemies."""

    def base_class(self) -> Any:
        return Character

    @abstractmethod
    def initial_mods(self) -> Sequence[Mod]:
        return []

    @abstractmethod
    def chassis(self) -> Chassis:
        return None

    @abstractmethod
    def additional_attributes(self) -> Dict[Attribute, int]:
        return {}

    @abstractmethod
    def max_health(self) -> int:
        return 0

    @abstractmethod
    def image_path(self) -> str:
        return ''

    @abstractmethod
    def character_name(self) -> str:
        return ''

    def build(self) -> Character:
        character_cls = self.base_class()
        char = character_cls(
            health=self.max_health(),
            image_path=self.image_path(),
            name=self.character_name())
        for mod in self.initial_mods():
            char.attempt_pickup(mod)

        attr_dict = self.additional_attributes()
        for attr in attr_dict:
            val = attr_dict[attr]
            char.increment_attribute(attr, val)

        # TODO(mick) - move positions to combat view
        char.set_position(200, 500, 150, 150)

        # TODO(dvirk) - set chassis for character

        return char


class CharacterFactory(Enum):
    HUMAN_PLAYER = 'human player'
    DRONE = 'drone'
    HARMLESS = 'harmless'
    USELESS = 'useless'

    def build(self) -> Character:
        data = _char_type_to_data[self]

        # We will need to refactor this. We should probably merge Character and
        # Enemy.
        if self == CharacterFactory.HUMAN_PLAYER:
            character_cls = Character
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
        char.ai = build_ai(char, data.ai_type)

        # TODO(dvirk) - set chassis for character

        return char


_char_type_to_data: Dict[CharacterFactory, CharacterData] = {
    CharacterFactory.DRONE: DRONE,
    CharacterFactory.HARMLESS: HARMLESS,
    CharacterFactory.USELESS: USLESS,
    CharacterFactory.HUMAN_PLAYER: HUMAN_PLAYER

}

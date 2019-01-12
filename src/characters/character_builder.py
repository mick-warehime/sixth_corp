from abc import abstractmethod
from typing import Any, Dict, Sequence

from characters.character_base import Character
from characters.chassis import Chassis
from characters.mods_base import Mod
from characters.states import Attribute


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
        char.set_position(200, 200, 150, 150)

        # TODO(dvirk) - set chassis for character

        return char

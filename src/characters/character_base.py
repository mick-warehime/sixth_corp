"""Basic class for player and enemies."""
from abc import abstractmethod
from typing import List, Sequence

from characters.abilities_base import Ability
from characters.character_position import Position
from characters.mods_base import Mod
from characters.states import AttributeType, State, Stateful


class Character(Stateful):
    """Stateful object with states and attributes affected by mods."""

    @property
    @abstractmethod
    def ai(self) -> 'AI':  # type: ignore
        pass

    @ai.setter
    def ai(self, ai: 'AI') -> None:  # type: ignore
        pass

    @property
    @abstractmethod
    def image_path(self) -> str:
        pass

    @property
    @abstractmethod
    def position(self) -> Position:
        pass

    @position.setter
    def position(self, pos: Position) -> None:
        pass

    @abstractmethod
    def attempt_pickup(self, mod: Mod) -> None:
        pass

    @abstractmethod
    def abilities(self) -> Sequence[Ability]:
        pass

    @abstractmethod
    def has_state(self, state: State) -> bool:
        pass

    @abstractmethod
    def increment_attribute(self, attribute: AttributeType, delta: int) -> None:
        pass

    @abstractmethod
    def get_attribute(self, attribute: AttributeType) -> int:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def select_move(self) -> 'Move':  # type: ignore
        pass

    @abstractmethod
    def set_targets(self, targets: List['Character']) -> None:
        pass

"""Abstract implementation of states and conditions."""
from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Union


class State(Enum):
    """Label for basic state condition requiring no internal logic to check.

     As a rule, we should define States whose absence is the default.. I.e.,
     ON_FIRE is a good State because Characters are usually not on fire. But
     IS_METALLIC is not good, since most Characters are assumed to be metallic.
     """
    ON_FIRE = 'on fire'
    FROZEN = 'frozen'
    SLEEPY = 'sleepy'

    def __str__(self) -> str:
        return self.value


class Attributes(Enum):
    HEALTH = 'health'
    MAX_HEALTH = 'maximum health'
    CREDITS = 'credits'
    CPU_SLOTS = 'CPU slots'

    def __str__(self) -> str:
        return self.value


class Skill(Enum):
    STEALTH = 'stealth'
    SPEECH = 'speech'
    MECHANICS = 'mechanics'


AttributeType = Union[Attributes, Skill]


class Status(metaclass=ABCMeta):
    """Contains information on the current state of an ingame object"""

    @abstractmethod
    def has_state(self, state: State) -> bool:
        """Whether object has a given state.

        If not otherwise set, default is False."""

    @abstractmethod
    def get_attribute(self, attribute: AttributeType) -> int:
        """Value associated with an Attribute.

        If not otherwise set, default value is 0."""

    @abstractmethod
    def increment_attribute(self, attribute: AttributeType, delta: int) -> None:
        """Increment an attribute by a fixed amount."""

    @abstractmethod
    def description(self) -> str:
        """Basic description of the object for logging and display purposes."""


class Stateful(metaclass=ABCMeta):
    """An in-game object with an in-game state."""

    @property
    @abstractmethod
    def status(self) -> Status:
        """This is what stores the object's state."""

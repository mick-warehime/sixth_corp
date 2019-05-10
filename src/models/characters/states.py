"""Abstract implementation of states and conditions."""
from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import (Callable, Dict, FrozenSet, Iterable, NamedTuple, Sequence,
                    Union, cast)

from frozendict import frozendict


class State(Enum):
    """Label for basic state condition requiring no internal logic to check.

     As a rule, we should define States whose absence is the default.. I.e.,
     ON_FIRE is a good State because Characters are usually not on fire. But
     IS_METALLIC is not good, since most Characters are assumed to be metallic.
     """
    ON_FIRE = 'on fire'
    FROZEN = 'frozen'
    SLEEPY = 'sleepy'
    IS_PLAYER = 'is player character'

    def __str__(self) -> str:
        return self.value


class Attributes(Enum):
    HEALTH = 'health'
    MAX_HEALTH = 'maximum health'
    CREDITS = 'credits'
    MAX_CPU = 'maximum CPU slots'
    CPU_AVAILABLE = 'CPU slots available'
    SHIELD = 'shield'

    def __str__(self) -> str:
        return self.value

    @property
    def is_permanent(self) -> bool:
        return self in _permanent_atts


_permanent_atts = {Attributes.MAX_HEALTH, Attributes.MAX_CPU}


class Skills(Enum):
    STEALTH = 'stealth'
    SPEECH = 'speech'
    MECHANICS = 'mechanics'


AttributeType = Union[Attributes, Skills]


class StatusEffect(NamedTuple):
    """Affects stateful attributes or grants/prevents states.

    Unlike States, a Stateful object may have more than one of the same status
    effects.

    Attributes:
        label: A short description of the effect. This should not contain the
            the attributes below.
        states_granted: States granted by the effect. As long as the stateful
            object has this effect, the specified states cannot be removed. When
            the effect is removed the states are also lost unless something else
            grants them.
        states_prevented: States prevented by the effect. As long as a stateful
            object has this effect, all states in states_prevented are set to
            False and may not be set to True. This preempts states granted by
            other StatusEffects.
        attribute_modifiers: Attributes which are modified by this effect.
            When Status.get_attribute is called, the corresponding
            modifier is added at the end (but is still set within specified
            bounds, as in implementation of BasicStatus). This means that a
            positive modifier effectively increases the lower bound of an
            attribute. Modifiers from multiple effects may stack. Modifiers
            disappear when the effect is removed.
    """
    label: str
    states_granted: FrozenSet[State]
    states_prevented: FrozenSet[State]
    attribute_modifiers: Dict[AttributeType, int]

    @classmethod
    def build(cls, label: str = 'unnamed effect',
              states_granted: Union[State, Iterable[State]] = (),
              states_prevented: Union[State, Iterable[State]] = (),
              attribute_modifiers: Dict[AttributeType, int] = None
              ) -> 'StatusEffect':
        """Constructor for StatusEffects.

        See class docstring for argument details.
        """

        if isinstance(states_granted, State):
            states_granted = (states_granted,)
        if isinstance(states_prevented, State):
            states_prevented = (states_prevented,)
        states_granted = frozenset(states_granted)
        states_prevented = frozenset(states_prevented)

        assert not (states_granted & states_prevented)

        if attribute_modifiers is None:
            attribute_modifiers = {}

        # To ensure immutability and a well defined hash
        attribute_modifiers = cast(Dict, frozendict(attribute_modifiers))

        return StatusEffect(label, states_granted, states_prevented,
                            attribute_modifiers)


class Status(metaclass=ABCMeta):
    """Contains information on the current state of an ingame object"""

    @abstractmethod
    def has_state(self, state: State) -> bool:
        """Whether object has a given state.

        If not otherwise set, default is False."""

    @abstractmethod
    def set_state(self, state: State, value: bool) -> None:
        """Assign (or remove) a given state."""

    @abstractmethod
    def get_attribute(self, attribute: AttributeType) -> int:
        """Value associated with an Attribute.

        If not otherwise set, default value is 0."""

    @abstractmethod
    def increment_attribute(self, attribute: AttributeType, delta: int) -> None:
        """Increment an attribute by a fixed amount."""

    @abstractmethod
    def add_status_effect(self, effect: StatusEffect) -> None:
        """Incorporate a StatusEffect.

        The same effect may be added multiple times.
        """

    @abstractmethod
    def remove_status_effect(self, effect: StatusEffect) -> None:
        """Remove a single copy of a StatusEffect."""

    @abstractmethod
    def active_effects(self, check: Callable[[StatusEffect], bool] = None
                       ) -> Sequence[StatusEffect]:
        """Get all status effects matching a certain filter condition.

         if check is None, then all status effects are returned.
         """


class Stateful(metaclass=ABCMeta):
    """An in-game object with an in-game state."""

    @property
    @abstractmethod
    def status(self) -> Status:
        """This is what stores the object's state."""

    @abstractmethod
    def description(self) -> str:
        """Basic description of the object for logging and display purposes."""

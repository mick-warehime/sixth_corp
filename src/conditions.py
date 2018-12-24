import abc

from states import Stateful, State, Attribute


class Condition(metaclass=abc.ABCMeta):
    """Represents a boolean statement that can be tested on HasState objects.
    """

    @abc.abstractmethod
    def check(self, target: Stateful) -> bool:
        """Evaluate this on a HasState object to determine condition value."""

    def __and__(self, other):
        if not isinstance(other, Condition):
            return NotImplemented
        return _And(self, other)


class _And(Condition):

    def __init__(self, *conditions: Condition):
        all_conds = set()
        for cond in (c for c in conditions if isinstance(c, _And)):
            all_conds.update(cond._conditions)

        all_conds.update(conditions)
        self._conditions = all_conds

    def check(self, target: Stateful):
        return all(c.check(target) for c in self._conditions)


class HasState(Condition):

    def __init__(self, state: State) -> None:
        self._state = state

    def check(self, target: Stateful):
        return target.has_state(self._state)


class IsDead(Condition):

    @classmethod
    def check(cls, target: Stateful) -> bool:
        return not target.get_attribute(Attribute.HEALTH)
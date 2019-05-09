from typing import Any, Callable, NamedTuple, Tuple

from models.characters.states import Attributes, Stateful

BoolFun = Callable[[Stateful], bool]


class _StatusConditionImpl(NamedTuple):
    """Internal implementation of StatusCondition.

    See the factory function status_condition for a summary.
    """
    and_clauses: Tuple[BoolFun, ...]

    def __call__(self, target: Stateful) -> bool:
        return all(clause(target) for clause in self.and_clauses)

    def __and__(self, other: Any) -> 'StatusCondition':
        if not isinstance(other, _StatusConditionImpl):
            return NotImplemented
        return _StatusConditionImpl(self.and_clauses + other.and_clauses)

    def __or__(self, other: Any) -> 'StatusCondition':
        if not isinstance(other, _StatusConditionImpl):
            return NotImplemented

        return _StatusConditionImpl((lambda t: self(t) or other(t),))

    def __invert__(self) -> 'StatusCondition':
        def not_self(target: Stateful) -> bool:
            return any(not clause(target) for clause in self.and_clauses)

        return _StatusConditionImpl((not_self,))


StatusCondition = _StatusConditionImpl


def status_condition(bool_fun: Callable[[Stateful], bool]) -> StatusCondition:
    """Factory function for StatusConditions.

    These are callables denoting boolean expressions single stateful objects.
    Also implemented are the logical AND (&), NOT (~) and OR (|) operations
    between StatusConditions.

    Args:
        bool_fun: The boolean function used to encode a single clause
            StatusCondition.

    Returns:
        A callable object equivalent to bool_fun that allows logical operations.

    """

    return _StatusConditionImpl((bool_fun,))


is_dead = status_condition(
    lambda s: s.status.get_attribute(Attributes.HEALTH) <= 0)
is_alive = ~ is_dead


def _is_hurt(target: Stateful) -> bool:
    value = target.status.get_attribute
    return value(Attributes.HEALTH) < value(Attributes.MAX_HEALTH)


is_hurt = status_condition(_is_hurt)

at_full_health = ~ is_hurt

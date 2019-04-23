import math

from models.characters.character_base import Character
from models.characters.states import Attributes
from models.characters.subroutines_base import Subroutine, build_subroutine


def repair(amount: int) -> Subroutine:
    """Self repair subroutine.

    Args:
        amount: Amount to repair. Must be positive.

    """
    assert amount > 0

    def use_fun(user: Character, target: Character) -> None:
        target.status.increment_attribute(Attributes.HEALTH, amount)

    def can_use_fun(user: Character, target: Character) -> bool:
        return user is target

    cpu_slots = max(1, amount // 2)
    time_slots = max(1, amount // 2)

    description = 'Repair {}'.format(amount)

    return build_subroutine(use_fun, can_use_fun, cpu_slots, time_slots,
                            description)


def direct_damage(damage: int, cpu_slots: int = None,
                  time_to_resolve: int = None,
                  label: str = '') -> Subroutine:
    """Subroutine to deal direct damage.

    The subroutine's user cannot target itself.

    Args:
        damage: Damage dealt, must be non-negative.
        cpu_slots: CPU slots required. Default is
            1 + damage // (2 * time_to_resolve+1).
        time_to_resolve:  Time to resolve. Default is int(sqrt(damage))
        label: A label prepended to the subroutine description.
    """

    if damage < 0:
        raise ValueError('damage must be non-negative.')
    if time_to_resolve is None:
        time_to_resolve = int(math.sqrt(damage))
    if cpu_slots is None:
        cpu_slots = 1 + damage // (2 * time_to_resolve + 1)

    def use_fun(user: Character, target: Character) -> None:
        target.status.increment_attribute(Attributes.HEALTH, -damage)

    def can_use_fun(user: Character, target: Character) -> bool:
        return user is not target

    description = '{} damage'.format(damage, time_to_resolve)
    if label:
        description = label + ' ' + description
    return build_subroutine(use_fun, can_use_fun, cpu_slots, time_to_resolve,
                            description)


def damage_over_time(damage_per_round: int, cpu_slots: int = None,
                     time_to_resolve: int = None,
                     label: str = '', duration: int = 2) -> Subroutine:
    """Subroutine to deal direct damage.

    The subroutine's user cannot target itself.

    Args:
        damage_per_round: Damage dealt per round, must be non-negative.
        cpu_slots: CPU slots required. Default is
            1 + damage // (2 * time_to_resolve+1).
        time_to_resolve:  Time to resolve the first damage round.
            Default is int(sqrt(damage))
        label: A label prepended to the subroutine description.
        duration: The number of rounds that the damage is dealt. Default is 2.
            Must be positive.
    """

    if damage_per_round < 0:
        raise ValueError('damage must be non-negative.')
    if duration <= 0:
        raise ValueError('duration must be positive.')

    if time_to_resolve is None:
        time_to_resolve = int(math.sqrt(damage_per_round))

    if cpu_slots is None:
        # CPU should grow with DPS, with less CPU for larger total time
        total_damage = damage_per_round * duration
        total_time = time_to_resolve + duration
        cpu_slots = 1 + total_damage // (2 * total_time)

    def use_fun(user: Character, target: Character) -> None:
        target.status.increment_attribute(Attributes.HEALTH, -damage_per_round)

    def can_use_fun(user: Character, target: Character) -> bool:
        return user is not target

    description = '{} damage/{} turns'.format(damage_per_round * duration,
                                              duration)
    if label:
        description = label + ' ' + description
    return build_subroutine(use_fun, can_use_fun, cpu_slots, time_to_resolve,
                            description, duration)

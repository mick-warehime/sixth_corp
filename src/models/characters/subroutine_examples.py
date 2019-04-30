import math

from models.characters.character_base import Character
from models.characters.states import Attributes, StatusEffect
from models.characters.subroutines_base import Subroutine, build_subroutine


def damage_target(amount: int, target: Character) -> None:
    """Deal damage to a target.

    This subroutine accounts for shields and other effects.
    """
    shields = target.status.get_attribute(Attributes.SHIELD)
    # amount = shield reduction + health reduction
    shield_reduction = min(shields, amount)  # shields can only go to zero.
    health_reduction = amount - shield_reduction

    target.status.increment_attribute(Attributes.SHIELD, -shield_reduction)
    target.status.increment_attribute(Attributes.HEALTH, -health_reduction)


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


def adjust_attribute(attribute: Attributes, amount: int = 0,
                     duration: int = None,
                     cpu_slots: int = None, time_to_resolve: int = 0,
                     is_buff: bool = None
                     ) -> Subroutine:
    """Adjust a permanent attribute over a finite duration.

    Permanent attributes may not be reduced below zero.

    Args:
        attribute: Attribute to be modified. attribute.is_permanent must be
            True.
        amount: How much to change the attribute by. May be positive or
            negative.
        duration: Number of rounds over which attribute is modified. Must be
            non-negative.
        cpu_slots: Number of CPU slots required to maintain the adjustment.
            Default is math.abs(amount).
        time_to_resolve: Number of rounds before modification is applied.
        is_buff: Whether the adjustment is a 'buff' (i.e. helpful). If True,
            then it may only be used on allies. If False, it may only be used
            on enemies. By default the subroutine may be used on both.
    """
    if duration < 0:
        raise ValueError('duration must be non-negative.')
    if not attribute.is_permanent:
        raise ValueError('Only permanent attributes may be modified.')

    description = '{} {}'.format(amount, attribute.value)
    if amount >= 0:
        description = '+' + description

    effect = StatusEffect.build(description,
                                attribute_modifiers={attribute: amount})

    def use_fun(user: Character, target: Character) -> None:
        target.status.add_status_effect(effect)

    def can_use(user: Character, target: Character) -> bool:
        if is_buff is None:
            return True
        elif is_buff:
            return target is user  # For now we assume user has no allies.
        else:
            return target is not user

    def after_effect(user: Character, target: Character) -> None:
        # If some other subroutine removes the effect first, this can cause
        # an error.
        target.status.remove_status_effect(effect)

    if cpu_slots is None:
        cpu_slots = abs(amount)

    description += ' {} rounds'.format(duration)

    return build_subroutine(use_fun, can_use, cpu_slots, time_to_resolve,
                            description, duration, after_effect=after_effect)


def shield_buff(amount: int, num_rounds: int = 1, cpu_slots: int = None,
                time_to_resolve: int = 0) -> Subroutine:
    """Adds a temporary damage shield buffer to the user.

    The shield fizzles either at the end of combat.

    Args:
        amount: Amount of shield added in a round. Must be non-negative.
        num_rounds: Number of rounds the buff is invoked. The total shield value
            does stacks. Must be positive.
        cpu_slots: CPU slots required. By default this is
            max(floor(sqrt(amount * duration) - sqrt(time_to_resolve)), 0)
        time_to_resolve: Time before shield occurs. By default the shield is
            instantaneous. Must be non-negative.
    """

    if amount < 0:
        raise ValueError('shield amount must be non-negative')
    if num_rounds < 1:
        raise ValueError('shield duration must be positive.')
    if time_to_resolve < 0:
        raise ValueError('shield time to resolve must be non-negative.')

    def can_use(user: Character, target: Character) -> bool:
        return user is target

    def use_fun(user: Character, target: Character) -> None:
        # Shield cannot decrease nor can it be made larger than amount.
        user.status.increment_attribute(Attributes.SHIELD, amount)

    if cpu_slots is None:
        cpu = math.sqrt(amount * num_rounds) - math.sqrt(time_to_resolve)
        cpu_slots = max(0, int(cpu))

    description = '+{} shield'.format(amount)
    if num_rounds > 1:
        description += ' for {} rounds'.format(num_rounds)
    return build_subroutine(use_fun, can_use, cpu_slots, time_to_resolve,
                            description, num_rounds - 1, False)


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
        damage_target(damage, target)

    def can_use_fun(user: Character, target: Character) -> bool:
        return user is not target

    description = '{} damage'.format(damage, time_to_resolve)
    if label:
        description = label + ' ' + description
    return build_subroutine(use_fun, can_use_fun, cpu_slots, time_to_resolve,
                            description)


def damage_over_time(damage_per_round: int, duration: int = 2,
                     cpu_slots: int = None, time_to_resolve: int = None,
                     label: str = '') -> Subroutine:
    """Subroutine to deal damage over multiple rounds.

    The subroutine's user cannot target itself.

    Args:
        damage_per_round: Damage dealt per round, must be non-negative.
        duration: The number of rounds that the damage is dealt. Default is 2.
            Must be positive.
        cpu_slots: CPU slots required. Default is
            1 + damage // (2 * time_to_resolve+1).
        time_to_resolve:  Number of rounds before first damage is dealt.
            Default is int(sqrt(damage))
        label: A label prepended to the subroutine description.
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
        damage_target(damage_per_round, target)

    def can_use_fun(user: Character, target: Character) -> bool:
        return user is not target

    description = '{} damage/{} turns'.format(damage_per_round * duration,
                                              duration)
    if label:
        description = label + ' ' + description
    return build_subroutine(use_fun, can_use_fun, cpu_slots, time_to_resolve,
                            description, duration, multi_use=True)

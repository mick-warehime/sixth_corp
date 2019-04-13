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

    description = 'Repair {} damage.'.format(amount)

    return build_subroutine(use_fun, can_use_fun, cpu_slots, time_slots,
                            description)


class FireLaser(Subroutine):

    def __init__(self, damage: int) -> None:
        assert damage > 0
        self._damage = damage

    def _use(self, user: Character, target: Character) -> None:
        target.status.increment_attribute(Attributes.HEALTH, -self._damage)

    def can_use(self, user: Character, target: Character) -> bool:
        return user is not target

    def description(self) -> str:
        return 'Fire laser! ({} damage)'.format(self._damage)

    def cpu_slots(self) -> int:
        return max(1, self._damage // 2)

    def time_slots(self) -> int:
        return max(1, self._damage // 2)

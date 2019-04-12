from typing import Any

from models.characters.character_base import Character
from models.characters.states import Attributes
from models.characters.subroutines_base import Subroutine


class Repair(Subroutine):

    def __init__(self, amount: int) -> None:
        assert amount > 0
        self._amount = amount

    def _use(self, user: Character, target: Character) -> None:
        target.status.increment_attribute(Attributes.HEALTH, self._amount)

    def can_use(self, user: Character, target: Character) -> bool:
        return user == target

    def describe_use(self, user: Character, target: Character) -> str:
        style = '{} repairs itself for {} damage.'
        return style.format(user.description(), self._amount)

    def description(self) -> str:
        return 'Repair {} damage.'.format(self._amount)

    def cpu_slots(self) -> int:
        return max(1, self._amount // 2)

    def time_slots(self) -> int:
        return max(1, self._amount // 2)


class FireLaser(Subroutine):

    def __init__(self, damage: int) -> None:
        assert damage > 0
        self._damage = damage

    def _use(self, user: Character, target: Character) -> None:
        target.status.increment_attribute(Attributes.HEALTH, -self._damage)

    def can_use(self, user: Character, target: Character) -> bool:
        return user is not target

    def describe_use(self, user: Character, target: Character) -> str:
        style = '{} fires a laser at {} for {} damage!'
        return style.format(user.description(),
                            target.description(), self._damage)

    def description(self) -> str:
        return 'Fire laser! ({} damage)'.format(self._damage)

    def cpu_slots(self) -> int:
        return max(1, self._damage // 2)

    def time_slots(self) -> int:
        return max(1, self._damage // 2)


class DoNothing(Subroutine):

    def __init__(self, harmless_value: int) -> None:
        self.value = harmless_value

    def _use(self, user: Character, target: Character) -> None:
        pass

    def can_use(self, user: Character, target: Character) -> bool:
        return True

    def describe_use(self, user: Character, target: Character) -> str:
        style = '{} from {} does nothing to {}'
        return style.format(self.description(), user.description(),
                            target.description())

    def description(self) -> str:
        return 'DoNothing {}'.format(self.value)

    def cpu_slots(self) -> int:
        return 1

    def time_slots(self) -> int:
        return 2

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DoNothing):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(('do_nothing', self.value))


class Unusable(Subroutine):

    def __init__(self, useless_value: int) -> None:
        self.value = useless_value

    def _use(self, user: Character, target: Character) -> None:
        pass

    def can_use(self, user: Character, target: Character) -> bool:
        return False

    def describe_use(self, user: Character, target: Character) -> str:
        style = '{} cant use this useless subroutine against {}'
        return style.format(user.description(),
                            target.description())

    def description(self) -> str:
        return 'Unusable subroutine {}'.format(self.value)

    def cpu_slots(self) -> int:
        return 1

    def time_slots(self) -> int:
        return 2

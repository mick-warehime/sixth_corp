from characters.conditions import FullHealth
from characters.states import Attributes, Stateful
from characters.subroutines_base import Subroutine


class Repair(Subroutine):

    def __init__(self, amount: int) -> None:
        assert amount > 0
        self._amount = amount

    def _use(self, user: Stateful, target: Stateful) -> None:
        target.increment_attribute(Attributes.HEALTH, self._amount)

    def can_use(self, user: Stateful, target: Stateful) -> bool:
        return user == target and not FullHealth().check(target)

    def describe_use(self, user: Stateful, target: Stateful) -> str:
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

    def _use(self, user: Stateful, target: Stateful) -> None:
        target.increment_attribute(Attributes.HEALTH, -self._damage)

    def can_use(self, user: Stateful, target: Stateful) -> bool:
        return user is not target

    def describe_use(self, user: Stateful, target: Stateful) -> str:
        style = '{} fires a laser at {} for {} damage!'
        return style.format(user.description(), target.description(),
                            self._damage)

    def description(self) -> str:
        return 'Fire laser! ({} damage)'.format(self._damage)

    def cpu_slots(self) -> int:
        return max(1, self._damage // 2)

    def time_slots(self) -> int:
        return max(1, self._damage // 2)


class Harmless(Subroutine):

    def __init__(self, harmless_value: int) -> None:
        self.value = harmless_value

    def _use(self, user: Stateful, target: Stateful) -> None:
        pass

    def can_use(self, user: Stateful, target: Stateful) -> bool:
        return True

    def describe_use(self, user: Stateful, target: Stateful) -> str:
        style = '{} from {} does nothing to {}'
        return style.format(self.description(), user.description(),
                            target.description())

    def description(self) -> str:
        return 'Harmless subroutine {}'.format(self.value)

    def cpu_slots(self) -> int:
        return 1

    def time_slots(self) -> int:
        return 2


class Useless(Subroutine):

    def __init__(self, useless_value: int) -> None:
        self.value = useless_value

    def _use(self, user: Stateful, target: Stateful) -> None:
        pass

    def can_use(self, user: Stateful, target: Stateful) -> bool:
        return False

    def describe_use(self, user: Stateful, target: Stateful) -> str:
        style = '{} cant use this useless subroutine against {}'
        return style.format(user.description(), target.description())

    def description(self) -> str:
        return 'Useless subroutine {}'.format(self.value)

    def cpu_slots(self) -> int:
        return 1

    def time_slots(self) -> int:
        return 2

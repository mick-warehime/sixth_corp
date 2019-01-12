from characters.abilities_base import Ability
from characters.conditions import FullHealth
from characters.states import Attribute, Stateful


class Repair(Ability):

    def __init__(self, amount: int) -> None:
        assert amount > 0
        self._amount = amount

    def _use(self, user: Stateful, target: Stateful) -> None:
        target.increment_attribute(Attribute.HEALTH, self._amount)

    def can_use(self, user: Stateful, target: Stateful) -> bool:
        return user == target and not FullHealth().check(target)

    def describe_use(self, user: Stateful, target: Stateful) -> str:
        style = '{} repairs itself for {} damage.'
        return style.format(user.description(), self._amount)

    def description(self) -> str:
        return 'Repair {} damage.'.format(self._amount)


class FireLaser(Ability):

    def __init__(self, damage: int) -> None:
        assert damage > 0
        self._damage = damage

    def _use(self, user: Stateful, target: Stateful) -> None:
        target.increment_attribute(Attribute.HEALTH, -self._damage)

    def can_use(self, user: Stateful, target: Stateful) -> bool:
        return user is not target

    def describe_use(self, user: Stateful, target: Stateful) -> str:
        style = '{} fires a laser at {} for {} damage!'
        return style.format(user.description(), target.description(),
                            self._damage)

    def description(self) -> str:
        return 'Fire laser! ({} damage)'.format(self._damage)


class Harmless(Ability):

    def __init__(self, harmless_value: int) -> None:
        self.value = harmless_value

    def _use(self, user: Stateful, target: Stateful) -> None:
        pass

    def can_use(self, user: Stateful, target: Stateful) -> bool:
        return True

    def describe_use(self, user: Stateful, target: Stateful) -> str:
        style = '{} from {} does nothing to {}'
        return style.format(self.description(), user.description(), target.description())

    def description(self) -> str:
        return 'Harmless ability {}'.format(self.value)


class Useless(Ability):

    def __init__(self, useless_value: int) -> None:
        self.value = useless_value

    def _use(self, user: Stateful, target: Stateful) -> None:
        pass

    def can_use(self, user: Stateful, target: Stateful) -> bool:
        return False

    def describe_use(self, user: Stateful, target: Stateful) -> str:
        style = '{} cant use this useless ability against {}'
        return style.format(user.description(), target.description())

    def description(self) -> str:
        return 'Useless ability {}'.format(self.value)

from characters.abilities_base import Ability
from characters.states import Stateful
from characters.conditions import FullHealth
from characters.states import Attribute


class Repair(Ability):

    def __init__(self, amount: int):
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

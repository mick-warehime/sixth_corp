from models.character_base import Character


class Move(object):
    def __init__(self, ability: 'Ability', user: Character,
                 target: Character) -> None:
        self._ability = ability
        self._user = user
        self._target = target

    def use(self) -> None:
        self._ability.use(self._user, self._target)

    def describe(self) -> str:
        return self._ability.describe_use(self._user, self._target)

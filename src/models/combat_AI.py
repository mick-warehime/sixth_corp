from models.character_base import Character


class Move(object):
    def __init__(self, ability: 'Ability', user: Character,
                 target: Character) -> None:
        self.ability = ability
        self.user = user
        self.target = target

    def use(self) -> None:
        self.ability.use(self.user, self.target)

    def describe(self) -> str:
        return self.ability.description()
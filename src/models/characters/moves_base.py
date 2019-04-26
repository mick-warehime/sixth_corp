from typing import NamedTuple

from models.characters.character_base import Character
from models.characters.subroutines_base import Subroutine


class Move(NamedTuple):
    subroutine: Subroutine
    user: Character
    target: Character

    def execute(self) -> None:
        self.subroutine.use(self.user, self.target)

    def description(self) -> str:
        return '{} {} --> {}'.format(self.user, self.subroutine.description(),
                                     self.target)

    def is_usable(self) -> bool:
        return self.subroutine.can_use(self.user, self.target)

    def __str__(self) -> str:
        return 'Move({} {} -> {})'.format(self.user,
                                          self.subroutine.description(),
                                          self.target)

    def __repr__(self) -> str:
        return str(self)

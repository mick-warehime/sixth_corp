from typing import NamedTuple

from characters.states import Stateful
from characters.subroutines_base import Subroutine


class Move(NamedTuple):
    subroutine: Subroutine
    user: Stateful
    target: Stateful

    def execute(self) -> None:
        self.subroutine.use(self.user, self.target)

    def description(self) -> str:
        return self.subroutine.describe_use(self.user, self.target)

    def is_usable(self) -> bool:
        return self.subroutine.can_use(self.user, self.target)

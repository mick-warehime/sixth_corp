from models.characters.mods_base import Mod
from models.characters.player import get_player, reset_player
from models.characters.states import AttributeType, Stateful
from models.scenes.scenes_base import Effect


class RestartGame(Effect):

    def execute(self) -> None:
        reset_player()


class IncrementAttribute(Effect):
    """Increment an attribute of some Stateful object."""

    def __init__(self, attribute: AttributeType, amount: int,
                 target: Stateful = None) -> None:
        """

        Args:
            attribute: Attribute to increment.
            amount: Amount.
            target: Stateful target. By default this is the player character.
        """
        self._target = target
        self._attribute = attribute
        self._amount = amount

    def execute(self) -> None:
        target = self._target if self._target is not None else get_player()
        target.status.increment_attribute(self._attribute, self._amount)


class AcquireMod(Effect):

    def __init__(self, mod: Mod) -> None:
        self._mod = mod

    def execute(self) -> None:
        get_player().chassis.attempt_store(self._mod)

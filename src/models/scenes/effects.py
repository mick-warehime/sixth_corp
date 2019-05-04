from models.characters.player import get_player, reset_player
from models.characters.states import AttributeType, Stateful


def restart_game() -> None:
    reset_player()


def increment_attribute(attribute: AttributeType, amount: int,
                        target: Stateful = None) -> None:
    """Increment an attribute of some Stateful object.

    Args:
        attribute: Attribute to increment.
        amount: Amount.
        target: Stateful target. By default this is the player character.
    """
    target = target if target is not None else get_player()
    target.status.increment_attribute(attribute, amount)

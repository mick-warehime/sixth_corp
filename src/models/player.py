"""Singleton Player Class.

    If you have a some function you would like to call
    function(player: Player) -> bool

    simply instantiate the singleton class

    from player import Player

    my_bool = function(Player())

    To reset the player call Player().reset()
"""
from models.character_base import Character

_INITIAL_HEALTH = 10


class Player(object):

    # Actual player implementation
    class __Player(Character):
        def __init__(self, health: int) -> None:
            super().__init__(health)

    _instance = None

    def __new__(cls) -> Character:
        if not Player._instance:
            Player.reset()
        return Player._instance

    @classmethod
    def reset(cls) -> None:
        Player._instance = Player.__Player(_INITIAL_HEALTH)

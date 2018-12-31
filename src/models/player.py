"""Singleton Player Class.

    If you have a some function you would like to call
    function(player: Player) -> bool

    simply instantiate the singleton class

    from player import Player

    my_bool = function(Player())

    To reset the player call Player().reset_player()
"""
from models.character_base import Character

_INITIAL_HEALTH = 10


class Player(object):

    # Actual player implementation
    class __Player(Character):
        def __init__(self, health: int) -> None:
            super().__init__(health)

    instance = None

    def __new__(cls):
        if not Player.instance:
            Player.reset_player()
        return Player.instance

    @classmethod
    def reset_player(cls):
        Player.instance = Player.__Player(_INITIAL_HEALTH)

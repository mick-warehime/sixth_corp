from models.character_base import Character


class World(object):
    __instance__: 'World' = None
    player: Character = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            cls.__instance__ = object.__new__(cls)
            cls.reset()

        return cls.__instance__

    @classmethod
    def reset(cls) -> None:
        cls.player = Character(health=15)


def get_world() -> World:
    return World()

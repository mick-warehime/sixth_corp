class World(object):
    __instance__: 'World' = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            cls.__instance__ = object.__new__(cls)
            cls.reset()

        return cls.__instance__

    @classmethod
    def reset(cls) -> None:
        pass


def get_world() -> World:
    return World()

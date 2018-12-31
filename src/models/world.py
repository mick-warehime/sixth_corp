from models.character_base import Character


class World(object):

    def __init__(self) -> None:
        self.player = Character(health=15)

    def reset(self) -> None:
        self.__init__()  # type: ignore

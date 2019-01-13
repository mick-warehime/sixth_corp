from abc import abstractmethod


class Move(object):

    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def describe(self) -> str:
        pass

    @abstractmethod
    def can_use(self) -> bool:
        pass

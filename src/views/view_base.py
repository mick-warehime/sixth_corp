from abc import abstractmethod


class View(object):

    @abstractmethod
    def update(self) -> None:
        """Updates the state of the view."""
        pass

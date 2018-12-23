from events import EventListener


class View(EventListener):
    def render(self) -> None:
        raise NotImplementedError("Subclasses must implement render()")

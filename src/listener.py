from events import Event


class Listener(object):

    def notify(self, event: Event) -> None:
        raise NotImplementedError("Subclasses must implement notify()")

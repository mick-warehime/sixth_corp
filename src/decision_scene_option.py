from world import World


class DecisionOption(object):

    def __init__(self, name: str) -> None:
        self.name = name

    def execute(self, world: World) -> None:
        world.current_scene = self.name

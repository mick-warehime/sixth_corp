class World(object):

    def __init__(self) -> None:
        self.scene_count = 0
        self.player = Character(health=15)

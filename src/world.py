class World(object):

    def __init__(self) -> None:
        self.scene_count = 0
        self.current_scene = 'new game'
        self.player = Character(health=15)

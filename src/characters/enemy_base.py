from characters.character_base import Character
from combat.ai.ai_base import AI
from combat.moves_base import Move

_ENEMY_IMAGE = 'src/images/drone.png'


class Enemy(Character):

    def __init__(self, health: int, name: str, image_path: str) -> None:
        super().__init__(health=health, name=name, image_path=image_path)
        self.ai: AI = None

    def select_move(self) -> Move:
        return self.ai.select_move()

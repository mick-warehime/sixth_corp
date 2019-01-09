from typing import List

from characters.abilities_base import Ability
from characters.ability_examples import FireLaser
from characters.character_base import Character

_ENEMY_IMAGE = 'src/images/drone.png'


class Enemy(Character):

    def __init__(self, health: int, name: str) -> None:
        super().__init__(health=health, name=name, image_path=_ENEMY_IMAGE)
        self.set_position(800, 100, 200, 150)

    def initial_abilities(self) -> List[Ability]:
        return [FireLaser(5)]

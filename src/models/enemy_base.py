from typing import List
from models.abilities_base import Ability
from models.ability_examples import FireLaser
from models.character_base import Character


class Enemy(Character):

    def initial_abilities(self) -> List[Ability]:
        return [FireLaser(5)]

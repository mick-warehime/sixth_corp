from typing import List

from characters.abilities_base import Ability
from characters.ability_examples import FireLaser
from characters.character_base import Character


class Enemy(Character):

    def initial_abilities(self) -> List[Ability]:
        return [FireLaser(5)]

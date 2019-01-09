from characters.ability_examples import FireLaser
from characters.character_base import Character
from characters.mods_base import GenericMod

_ENEMY_IMAGE = 'src/images/drone.png'


class Enemy(Character):

    def __init__(self, health: int, name: str) -> None:
        super().__init__(health=health, name=name, image_path=_ENEMY_IMAGE)
        self.set_position(800, 100, 200, 150)
        base_abilities = GenericMod(abilities_granted=(FireLaser(2)))
        self.attempt_pickup(base_abilities)

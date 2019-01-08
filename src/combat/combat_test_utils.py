from characters.character_base import Character
from characters.mod_examples import FireLaser
from characters.mods_base import GenericMod


class Combatant(Character):

    def __init__(self, health, abilities) -> None:
        super().__init__(health=health, name='combatant')

        base_abilities = GenericMod(abilities_granted=abilities)
        self.attempt_pickup(base_abilities)


def create_combat_group(group_size, health=10, damage=2):
    return [Combatant(health=health, abilities=(FireLaser(damage))) for _ in range(group_size)]

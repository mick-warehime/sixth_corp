from characters.character_base import Character
from characters.mod_examples import FireLaser
from characters.mods_base import GenericMod


def get_combatant(health, abilities, name) -> Character:
    char = Character(health, image_path='', name=name)
    mod = GenericMod(abilities_granted=abilities)
    char.attempt_pickup(mod)
    return char


def create_combat_group(group_size, health=10, damage=2, base_name='combatant'):
    return [get_combatant(health=health, abilities=(FireLaser(damage)), name=base_name + str(i))
            for i in range(group_size)]

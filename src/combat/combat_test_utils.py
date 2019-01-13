from characters.character_base import Character
from characters.character_examples import CharacterTypes
from characters.character_factory import build_character
from characters.character_impl import CharacterImpl
from characters.chassis import Chassis, TEMP_DEFAULT_SLOT
from characters.mod_examples import FireLaser
from characters.mods_base import GenericMod
from characters.states import Attribute


def get_combatant(health, abilities, name) -> Character:
    mod = GenericMod(attribute_modifiers={Attribute.MAX_HEALTH: health},
                     abilities_granted=abilities)
    chassis = Chassis({TEMP_DEFAULT_SLOT: 10}, mod)
    char = CharacterImpl(chassis, image_path='', name=name)

    return char


def create_combat_group(group_size, health=10, damage=2, base_name='combatant'):
    return [get_combatant(health=health, abilities=(FireLaser(damage)),
                          name=base_name + str(i))
            for i in range(group_size)]


def create_enemy(health: int = 10) -> Character:
    enemy = build_character(CharacterTypes.DRONE)
    cur_val = enemy.get_attribute(Attribute.HEALTH)
    enemy.increment_attribute(Attribute.HEALTH, -cur_val)
    enemy.increment_attribute(Attribute.HEALTH, health)
    return enemy

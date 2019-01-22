from characters.character_base import Character
from characters.character_examples import CharacterData, CharacterTypes
from characters.character_factory import build_character
from characters.chassis_examples import ChassisData
from characters.mod_examples import FireLaser
from characters.mods_base import ModData, Slots
from characters.states import Attribute
from combat.ai_factory import AIType


def get_combatant(health, subroutines, name, ai_type=AIType.Human) -> Character:
    mod_data = ModData(attribute_modifiers={Attribute.MAX_HEALTH: health},
                       subroutines_granted=subroutines, valid_slots=(Slots.ARMS,))
    chassis_data = ChassisData({Slots.ARMS: 10})
    char_data = CharacterData(chassis_data, name, (mod_data,), '', ai_type)

    return build_character(char_data)


def create_combat_group(group_size, health=10, damage=2, base_name='combatant'):
    return [get_combatant(health=health, subroutines=(FireLaser(damage)),
                          name=base_name + str(i))
            for i in range(group_size)]


def create_enemy(health: int = 10) -> Character:
    enemy = build_character(CharacterTypes.DRONE.data)
    cur_val = enemy.get_attribute(Attribute.HEALTH)
    enemy.increment_attribute(Attribute.HEALTH, -cur_val)
    enemy.increment_attribute(Attribute.HEALTH, health)
    return enemy

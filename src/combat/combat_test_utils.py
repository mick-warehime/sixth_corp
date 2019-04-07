from models.characters.character_base import Character
from models.characters.character_examples import CharacterData
from models.characters.character_impl import build_character
from models.characters.chassis_examples import ChassisData
from models.characters.mod_examples import FireLaser
from models.characters.mods_base import ModData, Slots
from models.characters.states import Attributes
from models.combat.ai_impl import AIType


def get_combatant(health, subroutines, name, ai_type=AIType.Human) -> Character:
    mod_data = ModData(attribute_modifiers={Attributes.MAX_HEALTH: health},
                       subroutines_granted=subroutines, valid_slots=(Slots.ARMS,))
    chassis_data = ChassisData({Slots.ARMS: 10})
    char_data = CharacterData(chassis_data, name, (mod_data,), '', ai_type)

    return build_character(char_data)


def create_combat_group(group_size, health=10, damage=2, base_name='combatant'):
    return [get_combatant(health=health, subroutines=(FireLaser(damage)),
                          name=base_name + str(i))
            for i in range(group_size)]



from characters.character_examples import CharacterData
from characters.character_impl import CharacterImpl
from models.characters.chassis_factory import build_chassis
from models.characters.mods_base import GenericMod
from models.characters.states import Attributes
from models.combat.ai_impl import build_ai


def build_character(data: CharacterData) -> CharacterImpl:
    chassis = build_chassis(data.chassis_data)

    ai = build_ai(data.ai_type)
    char = CharacterImpl(chassis, ai, data.image_path, name=data.name)
    ai.set_user(char)

    for mod_data in data.mods:
        mod = GenericMod(mod_data.states_granted, mod_data.attribute_modifiers,
                         mod_data.subroutines_granted, mod_data.valid_slots)
        assert char.inventory.can_store(mod), 'Mod cannot be picked up.'
        char.inventory.attempt_store(mod)

    health = char.status.get_attribute(Attributes.MAX_HEALTH)
    char.status.increment_attribute(Attributes.HEALTH, health)

    return char

from characters.character_examples import CharacterData
from characters.character_impl import CharacterImpl
from characters.character_position import Position
from characters.chassis_factory import build_chassis
from characters.mods_factory import build_mod
from characters.states import Attributes
from combat.ai_factory import AIType, build_ai


def build_character(data: CharacterData) -> CharacterImpl:
    chassis = build_chassis(data.chassis_data)
    char = CharacterImpl(chassis, image_path=data.image_path, name=data.name)

    for mod_data in data.mods:
        mod = build_mod(mod_data)
        assert char.inventory.can_store(mod), 'Mod cannot be picked up.'
        char.inventory.attempt_store(mod)

    health = char.status.get_attribute(Attributes.MAX_HEALTH)
    char.status.increment_attribute(Attributes.HEALTH, health)

    # TODO(#112) - move positions to combat view
    if data.ai_type == AIType.Human:
        pos = Position(200, 500, 150, 150)
    else:
        pos = Position(800, 300, 200, 150)
    char.position = pos
    char.ai = build_ai(char, data.ai_type)

    return char

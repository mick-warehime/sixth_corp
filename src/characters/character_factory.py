from pygame.rect import Rect

from characters.character_examples import CharacterData
from characters.character_impl import CharacterImpl
from characters.chassis_factory import build_chassis
from characters.mods_factory import build_mod
from characters.states import Attributes
from combat.ai_factory import AIType, build_ai
from views.artists.drawing_utils import rescale_horizontal, rescale_vertical


def build_character(data: CharacterData) -> CharacterImpl:
    chassis = build_chassis(data.chassis_data)

    ai = build_ai(data.ai_type)
    char = CharacterImpl(chassis, ai, data.image_path, name=data.name)
    ai.set_user(char)

    for mod_data in data.mods:
        mod = build_mod(mod_data)
        assert char.inventory.can_store(mod), 'Mod cannot be picked up.'
        char.inventory.attempt_store(mod)

    health = char.status.get_attribute(Attributes.MAX_HEALTH)
    char.status.increment_attribute(Attributes.HEALTH, health)

    return char

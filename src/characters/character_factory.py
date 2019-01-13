from typing import Union

from characters.character_examples import CharacterData, CharacterTypes
from characters.character_impl import CharacterImpl
from characters.character_position import Position
from characters.chassis_factory import build_chassis
from combat.ai.ai_factory import AIType, build_ai


def build_character(
        character: Union[CharacterTypes, CharacterData]) -> CharacterImpl:
    if isinstance(character, CharacterTypes):
        data = character.data
    else:
        data = character

    chassis = build_chassis(data.chassis_type)
    char = CharacterImpl(chassis, image_path=data.image_path,
                         name=data.name)

    # TODO(#112) - move positions to combat view
    if data.ai_type == AIType.Human:
        pos = Position(200, 500, 150, 150)
    else:
        pos = Position(800, 300, 200, 150)
    char.position = pos
    char.ai = build_ai(char, data.ai_type)

    return char

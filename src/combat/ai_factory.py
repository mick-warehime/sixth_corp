from enum import Enum

from characters.character_base import Character
from combat.ai_base import AI
from combat.random_ai import RandomAI
from combat.shuffle_ai import ShuffleAI


class AIType(Enum):
    Random = 'Random'
    Shuffle = 'Shuffle'
    Human = 'Human'


def build_ai(character: Character, ai_type: AIType) -> AI:
    if ai_type == AIType.Random:
        return RandomAI(character)
    elif ai_type == AIType.Shuffle:
        return ShuffleAI(character)
    elif ai_type == AIType.Human:
        return None  # type: ignore

    raise ValueError('Unexpected AIType {}'.format(ai_type))
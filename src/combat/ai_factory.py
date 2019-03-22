from enum import Enum

from combat.ai_base import AI
from combat.no_ai import NoAI
from combat.random_ai import RandomAI
from combat.shuffle_ai import ShuffleAI


class AIType(Enum):
    Random = 'Random'
    Shuffle = 'Shuffle'
    Human = 'Human'


def build_ai(ai_type: AIType) -> AI:
    if ai_type == AIType.Random:
        return RandomAI()
    elif ai_type == AIType.Shuffle:
        return ShuffleAI()
    elif ai_type == AIType.Human:
        return NoAI()

    raise ValueError('Unexpected AIType {}'.format(ai_type))

from enum import Enum

from characters.character_base import Character
from characters.player import get_player
from combat.ai.ai_base import AI
from combat.ai.random_ai import RandomAI
from combat.ai.shuffle_ai import ShuffleAI
from combat.moves_base import valid_moves


class AIType(Enum):
    Random = 'Random'
    Shuffle = 'Shuffle'


def build_ai(character: Character, ai_type: AIType) -> AI:
    moves = valid_moves(character, [get_player()])
    if ai_type == AIType.Random:
        return RandomAI(moves)
    elif ai_type == AIType.Shuffle:
        return ShuffleAI(moves)

    raise ValueError('Unexpected AIType {}'.format(ai_type))

from unittest import TestCase, mock
from combat.ai.shuffle_ai import ShuffleAI
from characters.ability_examples import Repair, FireLaser
from collections import defaultdict

REPAIR1 = Repair(1)
REPAIR2 = Repair(2)
LASER1 = FireLaser(1)
LASER2 = FireLaser(2)
MOVES = [REPAIR1, REPAIR2, LASER1, LASER2]


def mock_shuffle_moves():
    return MOVES.copy()


class ShuffleAITest(TestCase):

    def test_all_moves_get_used(self):
        ai = ShuffleAI(MOVES)
        ai.shuffle = mock_shuffle_moves
        for move in MOVES:
            actual_move = ai.select_move()
            self.assertEqual(actual_move, move)

    def test_moves_get_used_correct_number_of_times(self):
        n_shuffles = 3
        n_moves = len(MOVES)
        ai = ShuffleAI(MOVES, shuffle_size=n_shuffles)
        move_count = defaultdict(int)
        for _ in range(n_moves * n_shuffles):
            move = ai.select_move()
            move_count[move] += 1

        for move in move_count:
            self.assertEqual(move_count[move], n_shuffles)

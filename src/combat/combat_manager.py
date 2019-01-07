import logging
from itertools import product
from collections import namedtuple
from typing import Any, Sequence, Set, Tuple

from characters.character_base import Character
from characters.combat_AI import Move, all_moves


class CombatError(Exception):
    pass


class CombatState(object):
    pass


RewardFunc = Any
GroupMove = Sequence[Move]
MoveSet = Set[GroupMove]
CombatGroup = Sequence[Character]
CombatResult = Tuple[CombatState, int, bool]
CombatHistory = namedtuple('CombatHistory', ['state', 'attack', 'defense', 'result'])

HISTORY_FMT = '\n\nCOMBAT Turn {}:\nstate: {}\nattack: {}\ndefense: {}\nresult state: {}\nreward: {}\nis over?: {}\n'


def _default_reward_func(prev: CombatState, current: CombatState) -> int:
    return 0


class CombatManager(object):

    def __init__(self, attackers: CombatGroup, defenders: CombatGroup,
                 reward_func: RewardFunc = _default_reward_func) -> None:
        self._attackers = attackers
        self._defenders = defenders
        self._history: Sequence[CombatHistory] = []
        self._attackers_moves: MoveSet = None
        self._defenders_moves: MoveSet = None
        self._previous_state: CombatState = None
        self._reward_func: RewardFunc = reward_func

    def _current_state(self) -> CombatState:
        pass

    def state_space(self) -> Sequence[CombatState]:
        pass

    def attackers_moves(self) -> GroupMove:
        if self._attackers_moves is None:
            self._attackers_moves = self._enumerate_moveset(self._attackers, self._defenders)
        return self._attackers_moves

    def defenders_moves(self) -> GroupMove:
        if self._defenders_moves is None:
            self._defenders_moves = self._enumerate_moveset(self._defenders, self._attackers)
        return self._defenders_moves

    def step(self, attack_moves: GroupMove, defense_moves: GroupMove) -> CombatResult:
        'Apply the attackers move followed by the defenders moves.'
        previous_state = self._current_state()

        for attack_move in attack_moves:
            attack_move.use()

        for defense_move in defense_moves:
            defense_move.use()

        result = self._result(previous_state)
        history_record = CombatHistory(previous_state, attack_moves, defense_moves, result)
        self._update_history(history_record)

        return result

    def _result(self, prev_state: CombatState) -> CombatResult:
        state = self._current_state()
        reward = self._reward(prev_state, state)
        done = self._is_done()
        return (state, reward, done)

    def _reward(self, prev: CombatState, current: CombatState):
        return self._reward_func(prev, current)

    def _is_done(self) -> bool:
        return False

    def _enumerate_moveset(self, attackers: CombatGroup, defenders: CombatGroup) -> MoveSet:
        'All possible combinations of attack moves targeting all possible defenders'
        moveset = []
        for attacker in attackers:
            moveset.append(all_moves(attacker, defenders))
        return list(product(*moveset))

    def _update_history(self, record: CombatHistory) -> None:
        self._history.append(record)
        attack_descr = [m.describe() for m in record.attack]
        defense_descr = [m.describe() for m in record.defense]
        turn = len(self._history)

        history_description = HISTORY_FMT.format(turn, record.state, attack_descr, defense_descr, record.result[0],
                                                 record.result[1], record.result[2])
        print(history_description)
        logging.debug(history_description)

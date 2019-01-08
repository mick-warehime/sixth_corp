import logging
from typing import Sequence, Set, Tuple

from characters.character_base import Character
from characters.conditions import IsDead
from characters.combat_AI import Move, all_moves
from itertools import product

GroupMove = Sequence[Move]
GroupMoveSet = Set[GroupMove]
CombatGroup = Sequence[Character]
CombatHistory = Tuple[GroupMove, GroupMove]


class CombatManager(object):

    def __init__(self, attackers: CombatGroup, defenders: CombatGroup) -> None:
        self._attackers = attackers
        self._defenders = defenders
        self._history: Sequence[CombatHistory] = []
        self._attackers_moves: GroupMoveSet = None
        self._defenders_moves: GroupMoveSet = None

    def attackers_moves(self) -> GroupMove:
        if self._attackers_moves is None:
            self._attackers_moves = self._enumerate_moveset(self._attackers, self._defenders)
        return self._attackers_moves

    def defenders_moves(self) -> GroupMove:
        if self._defenders_moves is None:
            self._defenders_moves = self._enumerate_moveset(self._defenders, self._attackers)
        return self._defenders_moves

    def take_turn(self, attack_moves: GroupMove, defense_moves: GroupMove) -> None:
        for attack_move in attack_moves:
            attack_move.use()

        for defense_move in defense_moves:
            defense_move.use()

        attack_descr = [m.describe() for m in attack_moves]
        defense_descr = [m.describe() for m in defense_moves]
        logging.debug('ATTACK: {}'.format(attack_descr))
        logging.debug('DEFENSE: {}'.format(defense_descr))

    def is_done(self) -> bool:
        return self.attackers_lose() or self.defenders_lose()

    def _all_dead(self, group: CombatGroup) -> bool:
        for member in group:
            if not IsDead().check(member):
                return False
        return True

    def attackers_lose(self) -> bool:
        return self._all_dead(self._attackers)

    def defenders_lose(self) -> bool:
        return self._all_dead(self._defenders)

    def _enumerate_moveset(self, attackers: CombatGroup, defenders: CombatGroup) -> GroupMoveSet:
        'All possible combinations of attack moves targeting all possible defenders'
        moveset = []
        for attacker in attackers:
            moveset.append(all_moves(attacker, defenders))
        return list(product(*moveset))

import logging
from itertools import product
from typing import Sequence, Set, Tuple

from characters.character_base import Character
from characters.combat_AI import Move, valid_moves
from characters.conditions import IsDead

GroupMove = Sequence[Move]
GroupMoveSet = Set[GroupMove]
CombatGroup = Sequence[Character]
CombatHistory = Tuple[GroupMove, GroupMove, bool, bool]


def _describe_moves(moves: GroupMove) -> Sequence[str]:
    return [m.describe() for m in moves]


class CombatManager(object):
    """Manages combat state for generic groups of attackers and defenders."""

    def __init__(self, attackers: CombatGroup, defenders: CombatGroup) -> None:
        self._attackers = attackers
        self._defenders = defenders
        self.attackers_moves = self._enumerate_moveset(self._attackers, self._defenders)
        self.defenders_moves = self._enumerate_moveset(self._defenders, self._attackers)
        self.history: Sequence[CombatHistory] = []

    def take_turn(self, attack_moves: GroupMove, defense_moves: GroupMove) -> None:
        for move in attack_moves + defense_moves:
            assert move.can_use(), move.describe()
            move.use()

        attack_descr = _describe_moves(attack_moves)
        defense_descr = _describe_moves(defense_moves)
        logging.debug('ATTACK: {}'.format(attack_descr))
        logging.debug('DEFENSE: {}'.format(defense_descr))

        self.history.append(
            (attack_descr,
             defense_descr,
             self.attackers_lose(),
             self.defenders_lose()))

    def is_done(self) -> bool:
        return self.attackers_lose() or self.defenders_lose()

    def _all_dead(self, group: CombatGroup) -> bool:
        is_dead = IsDead()
        return all(is_dead.check(member) for member in group)

    def attackers_lose(self) -> bool:
        return self._all_dead(self._attackers)

    def defenders_lose(self) -> bool:
        return self._all_dead(self._defenders)

    def _enumerate_moveset(self, attackers: CombatGroup, defenders: CombatGroup) -> GroupMoveSet:
        'All possible combinations of attack moves targeting all possible defenders'
        moveset = []
        for attacker in attackers:
            attacks = valid_moves(attacker, defenders)
            # TODO(mick) - buffs can only target self not team. if we replace '[attacker]' with
            # 'attackers' here then we end up with friendly fire. potentially need to add
            # skill type = {attack, utility, defend, etc} and target accordingly. we could
            # also add the notion of 'side/team' to the character so can use does the right thing
            buffs = valid_moves(attacker, [attacker])
            moveset.append(attacks + buffs)
        return list(product(*moveset))

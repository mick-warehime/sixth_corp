from itertools import product
from typing import List, Sequence, Tuple

from events.events_base import EventManager, MoveExecutedEvent
from models.characters.character_base import Character
from models.characters.conditions import IsDead
from models.combat.moves_base import Move

GroupMove = Sequence[Move]
GroupMoveSet = Sequence[GroupMove]
CombatGroup = Sequence[Character]
CombatHistory = Tuple[Sequence[str], Sequence[str], bool, bool]


def _describe_moves(moves: GroupMove) -> Sequence[str]:
    return [m.description() for m in moves]


def valid_moves(user: Character, targets: Sequence[Character]) -> List[Move]:
    """All valid moves from a user to a sequence of targets"""
    return [Move(sub, user, target)
            for sub, target in
            product(user.chassis.all_subroutines(), targets)
            if sub.can_use(user, target)]


class CombatManager(object):
    """Manages combat state for generic groups of attackers and defenders."""

    def __init__(self, attackers: CombatGroup, defenders: CombatGroup) -> None:
        self._attackers = attackers
        self._defenders = defenders
        self.attackers_moves = self._enumerate_moveset(self._attackers,
                                                       self._defenders)
        self.defenders_moves = self._enumerate_moveset(self._defenders,
                                                       self._attackers)
        self.history: List[CombatHistory] = []

    def take_turn(self, attack_moves: GroupMove,
                  defense_moves: GroupMove) -> None:
        self._execute_moves(attack_moves, attacker=True)
        self._execute_moves(defense_moves, attacker=False)

        attack_descr = _describe_moves(attack_moves)
        defense_descr = _describe_moves(defense_moves)

        self.history.append((attack_descr, defense_descr, self.attackers_lose(),
                             self.defenders_lose()))

    def _execute_moves(self, moves: GroupMove, attacker: bool) -> None:
        for move in moves:
            assert move.is_usable(), move.description()
            EventManager.post(
                MoveExecutedEvent(move, is_attacker_move=attacker))
            move.execute()

    def is_done(self) -> bool:
        return self.attackers_lose() or self.defenders_lose()

    def _all_dead(self, group: CombatGroup) -> bool:
        is_dead = IsDead()
        return all(is_dead.check(member) for member in group)

    def attackers_lose(self) -> bool:
        return self._all_dead(self._attackers)

    def defenders_lose(self) -> bool:
        return self._all_dead(self._defenders)

    def _enumerate_moveset(self, attackers: CombatGroup,
                           defenders: CombatGroup) -> GroupMoveSet:
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

    def winners(self) -> CombatGroup:
        if self.defenders_lose():
            return self._attackers
        elif self.attackers_lose():
            return self._defenders

        assert False, 'Dont call winners if game is not done'

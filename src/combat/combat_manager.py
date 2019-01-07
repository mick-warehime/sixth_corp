from typing import Set, Sequence, Union

from itertools import product

from characters.character_base import Character
from characters.combat_AI import Move, all_moves

MoveSet = Set[Sequence[Move]]
CombatGroup = Sequence[Character]


class CombatError(Exception):
    pass


class CombatState(object):
    pass


class CombatResult(object):
    pass


class CombatManager(object):

    def __init__(self, attackers: CombatGroup, defenders: CombatGroup) -> None:
        self._attackers = attackers
        self._defenders = defenders
        self._attack_history: Sequence[Move] = []
        self._defense_history: Sequence[Move] = []
        self._next_attack: Sequence[Move] = None
        self._next_defense: Sequence[Move] = None
        self._attackers_moves: MoveSet = None
        self._defenders_moves: MoveSet = None

    def state(self) -> CombatState:
        pass

    def state_space(self) -> Sequence[CombatState]:
        pass

    def attackers_moves(self) -> Sequence[Move]:
        if self._attackers_moves is None:
            self._attackers_moves = self._enumerate_moveset(self._attackers, self._defenders)
        return self._attackers_moves

    def defenders_moves(self) -> Sequence[Move]:
        if self._defenders_moves is None:
            self._defenders_moves = self._enumerate_moveset(self._defenders, self._attackers)
        return self._defenders_moves

    def set_attack(self, attack: Union[Move, Sequence[Move]]) -> None:
        self._next_attack = attack

    def set_defense(self, defense: Union[Move, Sequence[Move]]) -> None:
        self._next_defense = defense

    def step(self) -> CombatResult:
        'Apply the attackers move followed by the defenders moves.'
        self._validate_moves()

        # do something

        self._clear_moves()

    def _validate_moves(self) -> None:
        if self._next_defense is None:
            raise CombatError('Defense move must be set before advancing combat')
        if self._next_attack is None:
            raise CombatError('Attack move must be set before advancing combat')

    def _clear_moves(self) -> None:
        self._next_attack = None
        self._next_defense = None

    def _enumerate_moveset(self, attackers: CombatGroup, defenders: CombatGroup) -> MoveSet:
        'All possible combinations of attack moves targeting all possible defenders'
        moveset = []
        for attacker in attackers:
            moveset.append(all_moves(attacker, defenders))
        return list(product(*moveset))

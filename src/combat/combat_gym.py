from collections import namedtuple
from itertools import product
from typing import Any, Sequence, Tuple

from characters.character_base import Character
from characters.states import Attribute, State
from combat.combat_manager_base import CombatGroup, CombatManager, GroupMove

RewardFunc = Any
CombatState = Sequence[int]
GroupCombatState = Sequence[CombatState]
CombatResult = Tuple[GroupCombatState, int, bool]


# TODO(mick): map character health to a smaller set of possible states (low, med, high)?
class CombatGym(CombatManager):
    ATTRIBUTE_STEP = 10
    ATTRIBUTE_MAX = 50
    REWARD_MAX = 10

    def __init__(
            self,
            attackers: CombatGroup,
            defenders: CombatGroup,
            character_attributes: Sequence[Attribute] = None,
            character_states: Sequence[State] = None) -> None:
        super().__init__(attackers, defenders)
        self._previous_state: CombatState = None

        self._character_attributes = [Attribute.HEALTH]
        if character_attributes is not None:
            self._character_attributes += character_attributes

        self._character_states = []
        if character_states is not None:
            self._character_states += character_states

    def current_state(self) -> GroupCombatState:
        """Current value of the relevant attributes and states of each attacker/defender."""
        group_state = []
        for group in [self._attackers, self._defenders]:
            for member in group:
                combat_state = []

                for attribute in self._character_attributes:
                    attr = self._clamped_attr_value(member, attribute)
                    combat_state.append(attr)

                for state in self._character_states:
                    val = int(member.has_state(state))
                    combat_state.append(val)

                group_state.append(tuple(combat_state))

        return tuple(group_state)

    def state_space(self) -> Sequence[GroupCombatState]:
        """State = (Health_state, attr_0, ..., attr_1"""
        n_attrs = len(self._character_attributes)
        n_states = len(self._character_states)

        max_attr = int(self.max_attribute())

        possible_attr_vals = list(range(max_attr + 1))
        possible_state_vals = [0, 1]

        inidividual_states = [possible_attr_vals] * n_attrs + [possible_state_vals] * n_states

        all_possible_ind_states = list(product(*inidividual_states))
        n_attackers = len(self._attackers)
        n_defenders = len(self._defenders)
        group_states = [all_possible_ind_states] * (n_attackers + n_defenders)
        return product(*group_states)

    def max_attribute(self) -> int:
        return int(CombatGym.ATTRIBUTE_MAX / CombatGym.ATTRIBUTE_STEP)

    def _clamped_attr_value(self, char: Character, attr: Attribute) -> int:
        """Limits the possible values of attributes to 0, 1, 2, ... MAX/STEP"""
        val = char.get_attribute(attr)
        for i in range(self.max_attribute() + 1):
            if val < i * CombatGym.ATTRIBUTE_STEP:
                break
        return i

    def step(self, attack_moves: GroupMove, defense_moves: GroupMove) -> CombatResult:
        'Apply the attackers move followed by the defenders moves.'
        self.take_turn(attack_moves, defense_moves)

        return self._result()

    def _result(self) -> CombatResult:
        reward = self._reward()
        done = self.is_done()
        return (self.current_state(), reward, done)

    def _reward(self):
        if self.attackers_lose():
            return CombatGym.REWARD_MAX
        elif self.defenders_lose():
            return -CombatGym.REWARD_MAX
        else:
            # Small reward for keeping the game going
            # Longer battles more fun??
            return 1

from models.characters.character_base import Character
from models.characters.character_examples import CharacterData
from models.characters.character_impl import build_character
from models.characters.conditions import IsDead
from models.characters.moves_base import Move
from models.characters.states import Attributes
from models.combat.combat_logic import CombatLogic


class SimulationError(Exception):
    pass


def _remove_user_cpu(move: Move) -> None:
    cpu_slots = move.subroutine.cpu_slots()
    assert cpu_slots <= move.user.status.get_attribute(
        Attributes.CPU_AVAILABLE)
    move.user.status.increment_attribute(Attributes.CPU_AVAILABLE, -cpu_slots)


def _return_user_cpu(move: Move) -> None:
    cpu_slots = move.subroutine.cpu_slots()
    move.user.status.increment_attribute(Attributes.CPU_AVAILABLE, cpu_slots)


class SimulationManager(object):
    """Utility class for simulating AI based combat"""

    def simulate(
            self,
            attacker_data: CharacterData,
            defender_data: CharacterData,
            n_runs: int = 1) -> float:
        """Runs {n_runs} combat simulations and reports attackers win frequency.
        """

        attacker_wins = 0
        for _ in range(n_runs):
            attacker = build_character(attacker_data)
            defender = build_character(defender_data)
            attacker_won = self._simulate_combat(attacker,  # type: ignore
                                                 defender)
            if attacker_won:
                attacker_wins += 1

        return attacker_wins * 1.0 / n_runs

    def _simulate_combat(self, attacker: Character,
                         defender: Character) -> bool:
        """Simulates combat between two enemies.

        Returns True if the attacker wins."""

        max_turns = 1000
        manager = CombatLogic([attacker, defender])
        is_dead = IsDead()
        for _ in range(max_turns):
            attack_move = attacker.ai.select_move([defender])
            defense_move = defender.ai.select_move([attacker])
            manager.start_round([attack_move, defense_move])
            manager.end_round()

            if is_dead.check(attacker) or is_dead.check(defender):
                return is_dead.check(defender)

        raise SimulationError(
            'Combat between {} and {} took more than {} turns'.format(
                attacker.description(), defender.description(),
                max_turns))

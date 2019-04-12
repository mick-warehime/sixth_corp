from models.characters.character_base import Character
from models.characters.character_examples import CharacterData
from models.characters.character_impl import build_character
from simulation.combat_manager_base import CombatManager


class SimulationError(Exception):
    pass


class SimulationManager(object):
    """Utility class for simulating AI based combat"""

    def simulate(
            self,
            attacker_data: CharacterData,
            defender_data: CharacterData,
            n_runs: int = 1) -> float:
        """Runs {n_runs} combat simulations and reports attackers win frequency."""

        attacker_wins = 0
        for _ in range(n_runs):
            attacker = build_character(attacker_data)
            defender = build_character(defender_data)
            attacker.ai.set_targets([defender])  # type: ignore
            defender.ai.set_targets([attacker])  # type: ignore
            attacker_won = self._simulate_combat(attacker,  # type: ignore
                                                 defender)
            if attacker_won:
                attacker_wins += 1

        return attacker_wins * 1.0 / n_runs

    def _simulate_combat(self, attacker: Character,
                         defender: Character) -> bool:
        """Simulates combat between two enemies and returns True if the attacker wins."""

        max_turns = 1000
        manager = CombatManager([attacker], [defender])
        for _ in range(max_turns):
            attack_move = attacker.ai.select_move()
            defense_move = defender.ai.select_move()
            manager.take_turn([attack_move], [defense_move])
            if manager.is_done():
                break

        if manager.is_done():
            return manager.winners() == [attacker]

        raise SimulationError(
            'Combat between {} and {} took more than {} turns'.format(
                attacker.description(), defender.description(),
                max_turns))

from characters.character_base import Character
from characters.character_examples import CharacterData
from characters.character_factory import build_character
from combat.combat_manager_base import CombatManager


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
        for i in range(n_runs):
            attacker = build_character(attacker_data)
            defender = build_character(defender_data)
            attacker.set_targets([defender])  # type: ignore
            defender.set_targets([attacker])  # type: ignore
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
        for i in range(max_turns):
            attack_move = attacker.select_move()
            defense_move = defender.select_move()
            manager.take_turn([attack_move], [defense_move])
            if manager.is_done():
                break

        if manager.is_done():
            return manager.winners() == [attacker]

        raise SimulationError(
            'Combat between {} and {} took more than {} turns'.format(
                attacker.status.description(), defender.status.description(),
                max_turns))

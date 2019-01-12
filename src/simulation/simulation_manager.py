from characters.enemies.enemy_base import Enemy
from characters.enemies.enemy_builder import EnemyBuilder
from combat.combat_manager_base import CombatManager


class SimluationError(Exception):
    pass


class SimulationManager(object):
    """Utility class for simulating AI based combat"""

    def simulate(
            self,
            attacker_builder: EnemyBuilder,
            defender_builder: EnemyBuilder,
            n_runs: int = 1) -> float:
        """Runs {n_runs} combat simulations and reports attackers win frequency."""
        
        attacker_wins = 0
        for i in range(n_runs):
            attacker = attacker_builder.build()
            defender = defender_builder.build()
            attacker.set_targets([defender])
            defender.set_targets([attacker])
            attacker_won = self._simulate_combat(attacker, defender)
            if attacker_won:
                attacker_wins += 1

        return attacker_wins * 1.0 / n_runs

    def _simulate_combat(self, attacker: Enemy, defender: Enemy) -> bool:
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

        raise SimluationError(
                'Combat between {} and {} took more than {} turns'.format(
                    attacker.description(), defender.description(), max_turns))



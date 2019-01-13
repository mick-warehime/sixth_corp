from unittest import TestCase

from characters.character_examples import CharacterTypes
from simulation.simulation_manager import SimulationError, SimulationManager


class TestSimulationManager(TestCase):

    def test_useless_enemy_always_loses(self):
        manager = SimulationManager()
        winrate = manager.simulate(CharacterTypes.HARMLESS,
                                   CharacterTypes.DRONE, n_runs=100)
        self.assertEqual(winrate, 0.0)

    def test_drone_always_wins(self):
        manager = SimulationManager()
        winrate = manager.simulate(CharacterTypes.DRONE,
                                   CharacterTypes.HARMLESS,
                                   n_runs=100)
        self.assertEqual(winrate, 1.0)

    def test_useless_enemies_never_finish_raises(self):
        manager = SimulationManager()
        with self.assertRaises(SimulationError):
            manager.simulate(CharacterTypes.HARMLESS,
                             CharacterTypes.HARMLESS, n_runs=100)

    def test_combatants_without_moves_raises(self):
        manager = SimulationManager()
        with self.assertRaises(AssertionError):
            manager.simulate(CharacterTypes.USELESS, CharacterTypes.USELESS,
                             n_runs=100)

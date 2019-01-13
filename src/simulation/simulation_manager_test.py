from unittest import TestCase

from characters.character_factory import CharacterFactory
from simulation.simulation_manager import SimluationError, SimulationManager


class TestSimulationManager(TestCase):

    def test_useless_enemy_always_loses(self):
        manager = SimulationManager()
        winrate = manager.simulate(CharacterFactory.HARMLESS,
                                   CharacterFactory.DRONE, n_runs=100)
        self.assertEqual(winrate, 0.0)

    def test_drone_always_wins(self):
        manager = SimulationManager()
        winrate = manager.simulate(CharacterFactory.DRONE,
                                   CharacterFactory.HARMLESS,
                                   n_runs=100)
        self.assertEqual(winrate, 1.0)

    def test_useless_enemies_never_finish_raises(self):
        manager = SimulationManager()
        with self.assertRaises(SimluationError):
            manager.simulate(CharacterFactory.HARMLESS,
                             CharacterFactory.HARMLESS, n_runs=100)

    def test_combatants_without_moves_raises(self):
        manager = SimulationManager()
        with self.assertRaises(AssertionError):
            manager.simulate(CharacterFactory.USELESS, CharacterFactory.USELESS,
                             n_runs=100)

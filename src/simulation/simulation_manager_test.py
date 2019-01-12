from unittest import TestCase
from characters.enemies.drone import DroneBuilder
from characters.enemies.harmless import HarmlessBuilder
from characters.enemies.useless import UselessBuilder
from simulation.simulation_manager import SimulationManager, SimluationError


class TestSimulationManager(TestCase):

    def test_useless_enemy_always_loses(self):
        manager = SimulationManager()
        winrate = manager.simulate(HarmlessBuilder(), DroneBuilder(), n_runs=100)
        self.assertEqual(winrate, 0.0)

    def test_drone_always_wins(self):
        manager = SimulationManager()
        winrate = manager.simulate(DroneBuilder(), HarmlessBuilder(), n_runs=100)
        self.assertEqual(winrate, 1.0)

    def test_useless_enemies_never_finish_raises(self):
        manager = SimulationManager()
        with self.assertRaises(SimluationError):
            manager.simulate(HarmlessBuilder(), HarmlessBuilder(), n_runs=100)

    def test_combatants_without_moves_raises(self):
        manager = SimulationManager()
        with self.assertRaises(AssertionError):
            manager.simulate(UselessBuilder(), UselessBuilder(), n_runs=100)

from unittest import TestCase
from models.mod_examples import AmuletOfSleepiness
from models.player import Player


class PlayerTest(TestCase):

    def setUp(self):
        Player.reset()

    def test_singleton(self):
        p1 = Player()
        p2 = Player()

        # Test pointer equality
        self.assertEqual(id(p1), id(p2))

    def test_add_mod_to_singleton(self):
        mod = AmuletOfSleepiness()
        initial_mod_count = len(Player().all_mods())
        Player().add_mod(mod)
        initial_mod_count_plus_one = len(Player().all_mods())

        self.assertEqual(initial_mod_count + 1, initial_mod_count_plus_one)

        mods = set(Player().all_mods())
        self.assertSetEqual(mods, set([mod]))

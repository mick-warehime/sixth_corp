from unittest import TestCase

from characters.ability_examples import FireLaser
from characters.states import Attribute
from combat.combat_manager_base import CombatManager
from combat.combat_test_utils import create_combat_group


class CombatManagerTest(TestCase):

    def test_enumerates_moves(self):
        attacker = create_combat_group(1)
        two_defenders = create_combat_group(2)
        manager = CombatManager(attackers=attacker, defenders=two_defenders)

        attack_moves = manager.attackers_moves()

        # two possible attacks (one per enemy)
        self.assertEqual(len(attack_moves), 2)

        # only one attacker (each possible move is a single move)
        self.assertEqual(len(attack_moves[0]), 1)
        self.assertEqual(len(attack_moves[1]), 1)

        # each attack move is just the laser ability
        for attacker_moveset in attack_moves:
            for move in attacker_moveset:
                self.assertIsInstance(move.ability, FireLaser)

        defense_moves = manager.defenders_moves()

        # one combo - each defender can only attack one target
        self.assertEqual(len(defense_moves), 1)

        # the possible defense move consists of two moves, each defender attacking
        self.assertEqual(len(defense_moves[0]), 2)

        # each defense move is just the laser ability
        for defender_moveset in defense_moves:
            for move in defender_moveset:
                self.assertIsInstance(move.ability, FireLaser)

    def test_step_applies_moves(self):
        health = 10
        damage = 2
        ndefenders = 2
        attacker = create_combat_group(1, health=health, damage=damage)
        two_defenders = create_combat_group(ndefenders, health=health, damage=damage)
        manager = CombatManager(attackers=attacker, defenders=two_defenders)

        defense_moves = manager.defenders_moves()
        attack_moves = manager.attackers_moves()
        manager.take_turn(attack_moves[0], defense_moves[0])

        # both defenders attack
        attacker_health = attacker[0].get_attribute(Attribute.HEALTH)
        self.assertEqual(attacker_health, health - ndefenders * damage)

        # attacker only hits one defender
        first_defender_health = attack_moves[0][0].target.get_attribute(Attribute.HEALTH)
        second_defender_health = attack_moves[1][0].target.get_attribute(Attribute.HEALTH)
        self.assertEqual(first_defender_health, health - damage)
        self.assertEqual(second_defender_health, health)

    def test_combat_result_indicates_combat_finished(self):
        health = 10
        damage = 2
        ndefenders = 2
        attacker = create_combat_group(1, health=health, damage=damage)
        two_defenders = create_combat_group(ndefenders, health=health, damage=damage)
        manager = CombatManager(attackers=attacker, defenders=two_defenders)

        defense_moves = manager.defenders_moves()
        attack_moves = manager.attackers_moves()
        manager.take_turn(attack_moves[0], defense_moves[0])

    def test_combat_finished(self):
        damage = 2
        ndefenders = 2
        attacker = create_combat_group(1, health=10, damage=damage)
        two_defenders = create_combat_group(ndefenders, health=0, damage=damage)
        manager = CombatManager(attackers=attacker, defenders=two_defenders)

        self.assertTrue(manager.is_done())
        self.assertTrue(manager.defenders_lose())
        self.assertFalse(manager.attackers_lose())

    def test_history_recorded(self):

        health = 10
        damage = 2
        ndefenders = 2
        attacker = create_combat_group(1, health=health, damage=damage)
        two_defenders = create_combat_group(ndefenders, health=health, damage=damage)
        manager = CombatManager(attackers=attacker, defenders=two_defenders)

        defense_moves = manager.defenders_moves()
        attack_moves = manager.attackers_moves()
        for i in range(3):
            manager.take_turn(attack_moves[0], defense_moves[0])

        self.assertTrue(manager.attackers_lose())
        self.assertEqual(len(manager.history), 3)

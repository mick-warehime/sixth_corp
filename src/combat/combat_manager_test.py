from unittest import TestCase

from characters.ability_examples import FireLaser
from characters.enemy_base import Character
from characters.mods_base import GenericMod
from characters.combat_AI import Move
from combat.combat_manager import CombatManager
from combat.combat_manager import CombatError


class Combatant(Character):

    def __init__(self, health, abilities) -> None:
        super().__init__(health=health, name='combatant')

        base_abilities = GenericMod(abilities_granted=abilities)
        self.attempt_pickup(base_abilities)


def create_combat_group(group_size):
    return [Combatant(health=10, abilities=(FireLaser(5))) for _ in range(group_size)]


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

    def test_no_moves_set_raises(self):
        attacker = create_combat_group(1)
        two_defenders = create_combat_group(2)
        manager = CombatManager(attackers=attacker, defenders=two_defenders)

        with self.assertRaises(CombatError):
            manager.step()

    def test_attack_unset_raises(self):
        attacker = create_combat_group(1)
        two_defenders = create_combat_group(2)
        manager = CombatManager(attackers=attacker, defenders=two_defenders)

        attack_moves = manager.attackers_moves()
        manager.set_attack(attack_moves[0])

        with self.assertRaises(CombatError):
            manager.step()

    def test_defense_unset_raises(self):
        attacker = create_combat_group(1)
        two_defenders = create_combat_group(2)
        manager = CombatManager(attackers=attacker, defenders=two_defenders)

        defense_moves = manager.defenders_moves()
        manager.set_defense(defense_moves[0])

        with self.assertRaises(CombatError):
            manager.step()

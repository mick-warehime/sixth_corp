from unittest import TestCase

from models.characters.states import Attributes, State
from simulation.combat_gym import CombatGym
from combat.combat_test_utils import create_combat_group


class CombatGymTest(TestCase):

    def test_attributes_get_added_to_states(self):
        health = 11
        damage = 2
        attacker = create_combat_group(1, health, damage)
        two_defenders = create_combat_group(2, health, damage)
        manager = CombatGym(attackers=attacker, defenders=two_defenders)

        self.assertEqual(manager.current_state(), ((2,), (2,), (2,)))

    def test_max_health(self):
        health = 10000
        damage = 2
        attacker = create_combat_group(1, health, damage)
        two_defenders = create_combat_group(2, health, damage)
        manager = CombatGym(attackers=attacker, defenders=two_defenders)

        max_health = manager.max_attribute()
        self.assertEqual(manager.current_state(), ((max_health,), (max_health,), (max_health,)))

    def test_state_space(self):
        health = 11
        damage = 2
        attacker = create_combat_group(1, health, damage)
        two_defenders = create_combat_group(2, health, damage)
        manager = CombatGym(attackers=attacker, defenders=two_defenders)
        states = list(manager.state_space())

        # When no special attributes/states are passed then only the health values
        # determine the states.

        # First state is all characters at min health
        self.assertEqual(states[0], ((0,), (0,), (0,)))

        # Last state is all characters at full health
        max_health = manager.max_attribute()
        self.assertEqual(states[-1], ((max_health,), (max_health,), (max_health,)))

        # 3 characters, each can have health states of 0, 1, ... , max_health
        n_states = (max_health + 1) ** 3  # 46656
        self.assertEqual(len(states), n_states)

    def test_state_space_two_attributes(self):
        health = 11
        damage = 2
        attacker = create_combat_group(1, health, damage)
        two_defenders = create_combat_group(2, health, damage)
        manager = CombatGym(
            attackers=attacker,
            defenders=two_defenders,
            character_attributes=[
                Attributes.MAX_HEALTH])
        states = list(manager.state_space())

        max_attr = manager.max_attribute()

        # Each attr has max_attr + 1 vals and there are 3 characters
        n_states = ((max_attr + 1) ** 2) ** 3
        self.assertEqual(len(states), n_states)

    def test_state_space_one_attr_one_state(self):
        health = 11
        damage = 2
        attacker = create_combat_group(1, health, damage)
        two_defenders = create_combat_group(2, health, damage)
        manager = CombatGym(
            attackers=attacker,
            defenders=two_defenders,
            character_states=[
                State.FROZEN])
        states = list(manager.state_space())

        # Each attr has max_attr + 1 vals and each state has two values (0,1) and
        # there are 3 characters
        max_attr = manager.max_attribute()
        n_states = ((max_attr + 1) * 2) ** 3
        self.assertEqual(len(states), n_states)

    def test_reward_ai_win(self):
        health = 3
        damage = 2
        attacker = create_combat_group(1, health, damage)
        two_defenders = create_combat_group(1, 2 * health, damage)
        manager = CombatGym(attackers=attacker, defenders=two_defenders)

        # First round of attacks gets player to 1 life
        defense_moves = manager.defenders_moves
        attack_moves = manager.attackers_moves
        (state, reward, done) = manager.step(attack_moves[0], defense_moves[0])

        self.assertEqual(state, ((1,), (1,)))
        self.assertEqual(reward, 1)
        self.assertFalse(done)

        # Enemy wins (positive reward for AI)
        (state, reward, done) = manager.step(attack_moves[0], defense_moves[0])
        self.assertEqual(state, ((0,), (1,)))
        self.assertEqual(reward, CombatGym.REWARD_MAX)
        self.assertTrue(done)

    def test_reward_ai_loss(self):
        health = 3
        damage = 2
        attacker = create_combat_group(1, 3 * health, damage)
        two_defenders = create_combat_group(1, health, damage)
        manager = CombatGym(attackers=attacker, defenders=two_defenders)

        # First round of attacks gets player to 1 life
        defense_moves = manager.defenders_moves
        attack_moves = manager.attackers_moves
        (state, reward, done) = manager.step(attack_moves[0], defense_moves[0])

        self.assertEqual(state, ((1,), (1,)))
        self.assertEqual(reward, 1)
        self.assertFalse(done)

        # Enemy wins (positive reward for AI)
        (state, reward, done) = manager.step(attack_moves[0], defense_moves[0])
        self.assertEqual(state, ((1,), (0,)))
        self.assertEqual(reward, -CombatGym.REWARD_MAX)
        self.assertTrue(done)

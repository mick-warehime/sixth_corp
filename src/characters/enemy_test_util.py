from characters.enemy_base import Enemy
from characters.enemy_examples import DroneBuilder
from characters.states import Attribute


def create_enemy(health: int = 10) -> Enemy:
    enemy = DroneBuilder().build()
    cur_val = enemy.get_attribute(Attribute.HEALTH)
    enemy.increment_attribute(Attribute.HEALTH, -cur_val)
    enemy.increment_attribute(Attribute.HEALTH, health)
    return enemy

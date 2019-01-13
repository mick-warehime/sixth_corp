from characters.character_builder import CharacterFactory
from characters.enemies.enemy_base import Enemy
from characters.states import Attribute


def create_enemy(health: int = 10) -> Enemy:
    enemy = CharacterFactory.DRONE.build()
    cur_val = enemy.get_attribute(Attribute.HEALTH)
    enemy.increment_attribute(Attribute.HEALTH, -cur_val)
    enemy.increment_attribute(Attribute.HEALTH, health)
    return enemy

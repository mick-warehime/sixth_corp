from unittest import TestCase

from controllers.pygame_collisions import point_collides_rect


class CollisionsTest(TestCase):

    def test_collide_point_origin_in_unit_square(self):
        self.assertTrue(point_collides_rect(0, 0, -1, -1, 2, 2))

    def test_collide_point_outside_unit_square(self):
        self.assertFalse(point_collides_rect(10, 10, -1, -1, 2, 2))

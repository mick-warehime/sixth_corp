from unittest import TestCase

from views.stack_utils import point_collides_stack_element, stack_position


class StackUtilsTest(TestCase):

    def test_click_center(self):
        for i in range(5):
            pos = stack_position(i)
            cx, cy = pos.center()
            self.assertTrue(point_collides_stack_element(i, cx, cy))

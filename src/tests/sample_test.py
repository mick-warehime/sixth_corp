from unittest import TestCase
from sample.first_file import function_to_test


class SampleTest(TestCase):

    def test_nothing(self):
        one = function_to_test()
        self.assertEqual(one, 1)

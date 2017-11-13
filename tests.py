import unittest
import person

class PersonCase(unittest.TestCase):
    def test_name(self):
        self.assertEqual("tom","John Smith")

unittest.main()
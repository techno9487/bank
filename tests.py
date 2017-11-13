import unittest
import person

class PersonCase(unittest.TestCase):
    def setUp(self):
        self.person = person.Person("John Smith","Password123",["1 somehwere lane"])
    def test_name(self):
        self.assertEqual(self.person.get_name(),"John Smith")
    def test_update_name(self):
        self.person.update_name("Sam")
        self.assertEqual(self.person.name,"Sam")
        self.person.name = "John Smith"

unittest.main()
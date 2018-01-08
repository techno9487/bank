import unittest
import person

class PersonCase(unittest.TestCase):
    def setUp(self):
        self.person = person.Person("John Smith","Password123",["1 somewhere lane"])
    def test_name(self):
        self.assertEqual(self.person.get_name(),"John Smith")
    def test_update_name(self):
        self.person.update_name("Sam")
        self.assertEqual(self.person.name,"Sam")
        self.person.name = "John Smith"
    def test_save(self):
        obj = self.person.save()
        self.assertEqual(obj,{"name":"John Smith","password":"Password123","address":["1 somewhere lane"]})
    def test_load(self):
        obj = {
            "name":"John Smith",
            "password":"password",
            "address":[None]
        }

        p = person.Person(None,None)
        p.load(obj)

        self.assertEqual(p.get_name(),"John Smith")
        self.assertEqual(p.password,"password")
        self.assertEqual(p.address,[None])

unittest.main()
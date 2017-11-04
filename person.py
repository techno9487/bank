
class Person(object):

    def __init__(self, name, password, address = [None, None, None, None]):
        self.name = name
        self.password = password
        self.address = address
        
    def get_address(self):
        return self.address

    def update_name(self, name):
        self.name = name
        
    def get_name(self):
        return self.name

    def check_password(self, password):
        if self.password == password:
            return True
        return False
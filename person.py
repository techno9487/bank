
class Person(object):

    def __init__(self, name, password, address = [None, None, None, None]):
        self.name = name
        self.password = password
        self.address = address
        
    def get_address(self):
        return self.address

    def update(self,name,address):
        self.name = name
        self.address = address
        
    def get_name(self):
        return self.name

    def check_password(self, password):
        if self.password == password:
            return True
        return False

    def save(self):
        return {"name":self.name,"password":self.password,"address":self.address}
    def load(self,obj):
        self.name  = obj["name"]
        self.password = obj["password"]
        self.address = obj["address"]
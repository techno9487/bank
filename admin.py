
from person import Person

class Admin(Person):
    
    def __init__(self, name, password, full_rights, address = [None, None, None, None]):
        super().__init__(name, password, address)
        self.full_admin_rights = full_rights

    def has_full_admin_right(self):
        return self.full_admin_rights

    def save(self):
        obj = super().save()
        obj["admin"] = self.full_admin_rights
        return obj
    def load(self,obj):
        super().load(obj)
        self.full_admin_rights = obj["admin"]


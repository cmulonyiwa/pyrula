from basics import BasicsTestCase
from app.models import Role, Permission


def add_perm(role):
    role.add_permission(Permission.FOLLOW)
    role.add_permission(Permission.WRITE)
    role.add_permission(Permission.COMMENT)
   
class RoleModelTestCase(BasicsTestCase):
    
    def test_add_permission(self):
        role = Role()       
        self.assertEqual(role.permissions, 0)
        add_perm(role)
        self.assertEqual(role.permissions , 7)

    def test_remove_permission(self):
        role = Role()
        self.assertEqual(role.permissions, 0) 
        add_perm(role) 
        role.remove_permission(Permission.FOLLOW)
        self.assertEqual(role.permissions, 6) 
        role.remove_permission(Permission.WRITE)
        self.assertEqual(role.permissions, 4) 
        role.remove_permission(Permission.COMMENT)
        self.assertEqual(role.permissions, 0)

    def test_reset_permission(self):
        role = Role()
        add_perm(role)
        role.reset_permission()
        self.assertEqual(role.permissions, 0)


        
from basics import BasicsTestCase
from app.models import Role, Permission, User


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


class UserModelTestCase(BasicsTestCase):
    def setUp(self):
        super().setUp()
        self.user = User(password='africa')

    def test_no_password_getter(self):
        with self.assertRaises(AttributeError):
            self.user.password

    def test_password_setter(self):
        self.assertTrue(self.user.password_hash is not None)

    def test_hashes_are_not_equal(self):
        user1 = User(password='africa')
        self.assertTrue(self.user.password_hash != user1)


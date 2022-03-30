import unittest
from app import create_app,db
from app.models import Role,User,Permissions

class  TestUserRole(unittest.TestCase):
	def setUp(self):
		self.app = create_app("testing")
		self.ctx = self.app.app_context()
		self.ctx.push()
		db.create_all()



	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.ctx.pop()

	def test_role_exist(self):
		role = Role(name="Mod")
		self.assertIsNotNone(role)

	def test_role(self):
		Role.insert_roles()
		role = Role(name="Admin1")
		db.session.add(role)
		db.session.commit()
		self.assertFalse(role.has_permission(Permissions.ADMIN))


	def test_add_perm(self):
		Role.insert_roles()
		role = Role(name="User1")

		role.add_permissions(Permissions.ADMIN)
		db.session.add(role)
		db.session.commit()
		self.assertTrue(role.permissions == 4)




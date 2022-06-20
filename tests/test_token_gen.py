import unittest
from app import create_app,db
from app.models import User

#test token generation capability
class TestTokenGen(unittest.TestCase):
	def setUp(self):
		self.app = create_app("testing")
		self.ctx = self.app.app_context()
		self.ctx.push()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		self.ctx.pop()
		db.drop_all()

	def test_token(self):
		u = User(email="hornet1@hornet",username="hornet2")
		db.session.add(u)
		db.session.commit()

		self.assertTrue(u.generate_confirm_token() != None)

	def test_auth(self):
		u = User(email="hornet1@hornet.com",username="hornet1")
		db.session.add(u)
		db.session.commit()
		self.assertTrue(u.confirm(u.generate_confirm_token()))

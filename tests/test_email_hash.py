import unittest
from app.models import User
from app import create_app,db

##test for user gravatar service
#for both hash and the full src
class TestEmailHash(unittest.TestCase):
	def setUp(self):
		self.app = create_app("testing")
		self.ctx = self.app.app_context()
		self.ctx.push()
		db.create_all()


	def tearDown(self):
		db.drop_all()
		db.session.remove()
		self.ctx.pop()


	def test_hash_exist(self):
		u = User(email="valid@valid.com")
		self.assertTrue(u.email_hash != None and len(u.email_hash) == 32)

	def test_gravatar_src(self):
		u = User(email="hornet@hornet")
		with self.app.test_request_context():
			self.assertIsNotNone(u.gravatar())

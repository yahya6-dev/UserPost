from app.models import User
import unittest
 

##test user model password capability
class TestPassword(unittest.TestCase):
	def test_password(self):
		u = User(password="hornet")

		self.assertIsNotNone(u.password_hash)

	def test_password_hash(self):
		u = User(password="king")
		u1 = User(password="king0")

		self.assertFalse(u.password_hash == u1.password_hash)


	def test_password_verify(self):
		u = User(password="hornet")

		self.assertTrue(u.verify("hornet"))


	def test_read_only(self):
		with self.assertRaises(AttributeError):
			u = User(password="cat")
			u.password

import unittest
from app import create_app,db
from flask import current_app

##basic testing to test app exist 
#and check configuration usage
class BasicAppTest(unittest.TestCase):
	def setUp(self):
		self.app = create_app("testing")
		self.ctx = self.app.app_context()
		self.ctx.push()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.ctx.pop()
	#test app exist
	def test_app_exist(self):
		self.assertTrue(current_app != None)

	#test app is testing
	def test_is_test(self):
		self.assertTrue(current_app.config.get("TESTING"))

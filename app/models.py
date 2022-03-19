from . import db
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from werkzeug.security import  check_password_hash,generate_password_hash
from flask import request
from flask_login import UserMixin,AnonymousUserMixin
from datetime import datetime

##users role only two exist admin and normal users
##default permission for normal user
class Role(db.Model):
	__tablename__="roles"
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String,unique=True)
	permissions = db.Column(db.Integer)
	default = db.Column(db.Boolean,default=False)

	##check permission so as to not be None
	def __init__(self,**kargs):
		super(Role,self).__init__(**kargs)
		if not self.permissions:
			self.permissions = 0


##user model implementation
##containing gravatar link,username
class User(db.Model):
	__tablename__="users"
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(64),unique=True)
	password_hash = db.Column(db.String(128))
	location = db.Column(db.String(20),index=True)
	DOB = db.Column(db.DateTime)
	last_seen = db.Column(db.DateTime,default=datetime.utcnow)
	confirm = db.Column(db.Integer,default=False)


	@property
	def password(self):
		raise AttributeError("password is unreadable")

	@password.setter
	def password(self,password):
		self.password_hash = generate_password_hash(password)


	def verify(self,password):
		return check_password_hash(self.password_hash,password)


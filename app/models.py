from . import db,login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from werkzeug.security import  check_password_hash,generate_password_hash
from flask import request,current_app as app
from flask_login import UserMixin,AnonymousUserMixin
from datetime import datetime
import hashlib

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
class User(UserMixin,db.Model):
	__tablename__="users"
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(64),unique=True)
	password_hash = db.Column(db.String(128))
	location = db.Column(db.String(20),index=True)
	DOB = db.Column(db.DateTime)
	last_seen = db.Column(db.DateTime,default=datetime.utcnow)
	confirmed = db.Column(db.Integer,default=False)
	email_hash = db.Column(db.String(32))
	email = db.Column(db.String(64),unique=True,nullable=False)

	def __init__(self,**kargs):
		super(User,self).__init__(**kargs)
		if not self.email_hash and self.email:
			self.email_hash = self.gravatar_hash()

	##manage account verification of account
	def generate_confirm_token(self,expires_in=3600):
		s = serializer(app.config.get("SECRET_KEY"),expires_in=expires_in)
		return s.dumps({"id":self.id})

	##confirm the token generated earlier
	def confirm(self,token):
		s = serializer(app.config.get("SECRET_KEY"))

		try:
			data = s.loads(token)
		except:
			return False

		if data.get("id") != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		db.session.commit()

		return True

	@property
	def password(self):
		raise AttributeError("password is unreadable")

	@password.setter
	def password(self,password):
		self.password_hash = generate_password_hash(password)


	def verify(self,password):
		return check_password_hash(self.password_hash,password)


	def gravatar_hash(self):
		return hashlib.md5(self.email.encode("utf-8").lower()).hexdigest()

	def gravatar(self,size=50,rating="g",default="identicon"):
		if request.is_secure:
			url = "https://secure.gravatar.com/avatar"
		else:
			url = "http://gravatar.com/avatar"

		hash = self.email_hash or self.gravatar_hash()
		return "{url}/{hash}&s={size}&r={rating}&d={default}".format(url=url,hash=hash,size=size,rating=rating,default=default)


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

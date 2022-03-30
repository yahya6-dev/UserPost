from . import db,login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from werkzeug.security import  check_password_hash,generate_password_hash
from flask import request,current_app as app
from flask_login import UserMixin,AnonymousUserMixin
from datetime import datetime
import hashlib
import bleach
from markdown import markdown

##all user role
class Permissions:
	WRITE = 1
	LIKE  = 2
	ADMIN = 4


##users role only two exist admin and normal users
##default permission for normal user
class Role(db.Model):
	__tablename__="roles"
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String,unique=True)
	permissions = db.Column(db.Integer)
	default = db.Column(db.Boolean,default=False)
	users_id = db.relationship("User",backref="role",lazy="dynamic")

	##check permission so as to not be None
	def __init__(self,**kargs):
		super(Role,self).__init__(**kargs)
		if not self.permissions:
			self.permissions = 0

	def has_permission(self,permission):
		return self.permissions & permission == permission

	def add_permissions(self,permissions):
		if not self.has_permission(permissions):
			self.permissions += permissions
	@staticmethod
	def insert_roles():
		roles = {"User":[Permissions.WRITE,Permissions.LIKE],
			"Admin":[Permissions.WRITE,Permissions.LIKE,Permissions.ADMIN]

		}

		for field in roles:
			role = Role.query.filter_by(name=field).first()
			if not role:
				role = Role(name=field)
			for permission in roles[field]:
				role.add_permissions(permission)
			db.session.add(role)

		db.session.commit()

##user post model interspersed with markdown
##for text preview and editing
class Post(db.Model):
	__tablename__="posts"
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(64))
	post_body = db.Column(db.Text())
	post_html = db.Column(db.Text())
	timestamp = db.Column(db.DateTime,default=datetime.utcnow)
	user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

	@staticmethod
	def on_change_post(target,value,old,initiator):
		allowed_tags = ["h1","h2","h3","h4","h5","kbd","code","div","img","br","p","video","audio"]
		target.post_html = bleach.linkify(bleach.clean(markdown(value,output_format="html"),strip=True,tags=allowed_tags))

#bind listener to change post_body to post_html with rich text
db.event.listen(Post.post_body,"set",Post.on_change_post)

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
	role_id = db.Column(db.Integer,db.ForeignKey("roles.id"))
	posts = db.relationship("Post",backref="author",lazy="dynamic")

	def __init__(self,**kargs):
		super(User,self).__init__(**kargs)
		if not self.email_hash and self.email:
			self.email_hash = self.gravatar_hash()

	def can(self,permission):
		return self.role.has_permission(permission)

	def is_admin(self):
		return self.role.has_permission(Permission.ADMIN)

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


class Anonymous(AnonymousUserMixin):
	def can(self,permission):
		return False
	def is__admin(self):
		return False

login_manager.anonymous_user = Anonymous

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,PasswordField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_pagedown.fields import PageDownField
from ..models import User

##main login form to be displayed  first to user
class LoginForm(FlaskForm):
	username = StringField("Username",validators=[DataRequired()])
	confirm = SubmitField("Confirm")

##second screen to be displayed to the user after entering valid username
class LoginFormImg(FlaskForm):
	password = PasswordField("Password",validators=[DataRequired()])
	login = SubmitField("Login")


##main registration form
class RegisterForm(FlaskForm):
	locations = ["Kano","Katsina","Kaduna","Abuja"]
	username = StringField("Username",validators=[DataRequired()])
	password1 = StringField("Password",validators=[DataRequired()])
	password2 = StringField("Confirm",validators=[EqualTo("password1",message="mismatch")])
	email = StringField("Email",validators=[DataRequired(),Email()])
	location = SelectField("Location")
	register = SubmitField("Register")

	def __init__(self,**kargs):
		super(RegisterForm,self).__init__(**kargs)
		self.location.choices = self.locations 

	def validate_username(self,username):
		if User.query.filter_by(username=username.data).first():
			raise ValidationError("already taken")

	def validate_email(self,email):
		if User.query.filter_by(email=email.data).first():
			raise ValidationError("Email registered")
##main post form
class PostForm(FlaskForm):
	title = StringField("title")
	post = PageDownField("Post")
	submit = SubmitField("Post") 

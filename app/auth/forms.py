from flask_wtf import FlaskForm
from wtform import StringField,SubmitField,PasswordField
from wtform.validators import DataRequired,Length,Email
from flask_pagedown.fields import PageDownField

##main login form to be displayed  first to user
class LoginForm(FlaskForm):
	username = StringField("Username",validators=[DataRequired()])
	submit = Submit("Confirm")

##second screen to be displayed to the user after entering valid username
class LoginFormImg(Flask):
	password = PasswordField("Password",validators=[DataRequired()])
	submit = SubmitField("Login")


##main registration form
class RegisterForm(FlaskForm):
	locations = ["Kano","Katsina","Kaduna","Abuja"]
	username = StringField("Username")
	password1 = StringField("Password")
	password2 = StringField("Confirm")
	email = StringField("Email")
	location = SelectForm(Location)

	def __init__(self,**kargs):
		super(RegistrationForm,self).__init__(**kargs)
		self.location.choices = self.locations 

##main post form
class PostForm(FlaskForm):
	title = StringField("title")
	post = PageDownField("Post")
	submit = SubmitField("Post") 

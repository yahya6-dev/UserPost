from wtforms import SubmitField,StringField
from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
	title = StringField()
	post_body = PageDownField(validators=[DataRequired()])
	submit = SubmitField()




from wtforms import SubmitField,StringField
from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired
#main post form
class PostForm(FlaskForm):
	title = StringField()
	post_body = PageDownField(validators=[DataRequired()])
	submit = SubmitField()


##comment form
class CommentForm(FlaskForm):
	content = PageDownField(validators=[DataRequired()])
	submit = SubmitField()


from . import main
from flask import render_template,request
from .forms import PostForm,CommentForm
from ..models import User,Post,Permissions,db
from flask_login import current_user
from flask import flash,url_for,redirect


@main.route("/",methods=["POST","GET"])
def index():
	form = PostForm()
	comment_form = CommentForm()

	if form.validate_on_submit()  and current_user.is_authenticated:
		post = Post(post_body=form.post_body.data,title=form.title.data,author=current_user._get_current_object())
		db.session.add(post)
		db.session.commit()
		flash("Posted Successfully")
		return redirect(url_for("main.index"))

	page = request.args.get("page",1,type=int)
	paginations = Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=20,error_out=True)
	return render_template("main/index.html",post_form=form,paginations=paginations,posts=paginations.items,comment_form=comment_form)


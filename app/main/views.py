from . import main
from flask import render_template,request
from .forms import PostForm
from ..models import User,Post

@main.route("/",methods=["POST","GET"])
def index():
	form = PostForm()
	page = request.args.get("page",1,type=int)
	paginations = Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=20,error_out=True)
	return render_template("main/index.html",post_form=form,paginations=paginations,posts=paginations.items)

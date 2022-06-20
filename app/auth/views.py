from .forms import PostForm,RegisterForm,LoginFormImg,LoginForm
from . import auth
from flask import render_template,url_for,redirect,session,flash,abort,request,current_app
from flask_login import login_required,logout_user,login_user,current_user
from ..models import User,db
from ..mails import send_mail 

##first route to handle username then issue redirect to log2
@auth.route("/login",methods=["GET","POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			return redirect(url_for("auth.login1",username=form.username.data))
		else:
			flash("Invalid User")
			return redirect(url_for("auth.login"))
	return render_template("login/login.html",form=form)

##other route to process the password 
@auth.route("/login1/<username>",methods=["POST","GET"])
def login1(username):
	form = LoginFormImg()

	user = User.query.filter_by(username=username).first()
	if not user:
		abort(404)
	if form.validate_on_submit():
		if user.verify(form.password.data):
			login_user(user,form.remember.data)
			next = request.args.get("next")
			if not next or  next.startswith("/"):
				next = url_for("main.index")
			flash("Successfully login")
			return redirect(next)

		else:
			flash("Incorrect password")
			return redirect(url_for("auth.login1",username=username))

	return render_template("login/login1.html",form=form,user=user)

#main route to deal with logout
@auth.route("/logout",methods=["GET","POST"])
@login_required
def logout():
	user = current_user._get_current_object()
	logout_user()
	return redirect(url_for("main.index"))

#registration main route
@auth.route("/register",methods=["POST","GET"])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(username=form.username.data,
		email = form.email.data,password=form.password1.data,location=form.location.data)
		db.session.add(user)
		db.session.commit()
		send_mail(current_app.config.get("UserPost_Admin"),form.email.data,"Account Confirmation","mail/register_confirm",user=user,token=user.generate_confirm_token())
		login_user(user,True)
		return redirect(url_for("auth.unconfirmed",user=user))

	return render_template("register/register.html",form=form)

#redirect logged user from accessing login route
@auth.before_app_request
def before_request():
	#if current_user.is_authenticated and  not current_user.confirmed:
	#	return redirect(url_for("auth.unconfirmed"))

	if request.endpoint in [ "auth.login","auth.login1"] and current_user.is_authenticated:
		return redirect(url_for("main.index"))


##unconfirmed route handler
@auth.route("/unconfirmed")
def unconfirmed():
	return render_template("register/unconfirmed.html",user=current_user)

#resend confirmation token
@auth.route("/resend")
@login_required
def resend():
	token = current_user.generate_confirm_token()
	app = current_app._get_current_object()
	send_mail(app.config.get("UserPost_Admin"),current_user.email,"account confirmation","mail/register_confirm",token=current_user.generate_confirm_token(),user=current_user)
	return redirect(url_for("auth.unconfirmed"))
##confirm user
@auth.route("/confirm/<token>")
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for("main.index"))
	if current_user.confirm(token):
		flash("account confirmed")
		return redirect(url_for("main.index"))
	else:
		flash("token expired")
		return redirect(url_for("auth.unconfirmed"))

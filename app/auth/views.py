from .forms import *
from . import auth
from flask import render_template,url_for,redirect


@auth.login("/login",methods=["GET","POST"])
def login


@auth.logout("/logout",methods=["GET","POST"])


from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database import users_collection
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import  create_access_token, set_access_cookies, unset_jwt_cookies

auth_bp = Blueprint("auth",__name__)

@auth_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")




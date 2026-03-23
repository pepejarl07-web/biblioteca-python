from http.client import responses

from flask import Blueprint, render_template, request, redirect, url_for, flash
from .database import users_collection
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import  create_access_token, set_access_cookies, unset_jwt_cookies

auth_bp = Blueprint("auth",__name__) #creamos blueprint xa agrupar rutas de autenticacion

@auth_bp.route("/register", methods=["GET","POST"]) # GET devuelve el formulario vacio
def register():
    if request.method=="POST": # obtiene datos del formulario
        username=request.form.get("username")
        password=request.form.get("password")

        #validaciones
        errors={}
        if not username:
            errors["username"] = "El nombre de usuario es obligatorio."
        if not password:
            errors["password"] = "La contraseña es obligatoria"
        elif len(password) < 6:
            errors["password"] = "La contraseña tiene que tener al mnenos 6 caracteres"

        # verificar si el usuario ya existe
        if not errors and users_collection.find_one({"username": username}):
            errors["username"] = "El nombre de usuario ya está en uso"

        if errors:
            return render_template("auth/register.html", errors=errors, data={"username":username})

        #crear nuevo usuario con contraseña hasheada
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({   # guarda el nuevo usuario en mongoDB
                                    "username":username,
                                    "password":hashed_password, #con la contraseña hasheada
                                    "role": request.form.get("role","user") # viene del select del formulario
                                    })
        flash("Usuario registrado correctamente. Ahora puedes iniciar sesion.", "success")
        return redirect(url_for("auth.login"))
    #Si es GET se muestra formulario vacío
    return render_template("auth/register.html", errors={}, data={})

#Ruta de inicio de sesion
@auth_bp.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        #Buscar al usuario en la base de datos
        user = users_collection.find_one({"username":username})

        #verificar credenciales
        if user and check_password_hash(user["password"], password):
            #Crear token JWT con el id del user como identidad
            access_token = create_access_token(
                                        identity=str(user["_id"]),
                                        additional_claims={"role": user.get("role","user")})

            response = redirect(url_for("books.list_books"))
            set_access_cookies(response, access_token)          #guarda el token en una cookie!
            flash("inicio de sesion exitoso", "success")
            return response
        else:
            flash("Usuario o contraseña incorrectos")
            return render_template("auth/login.html")

    #si es GET muestra el formulario de login
    return render_template("auth/login.html")

#Ruta de cierre de sesión
@auth_bp.route("/logout")
def logout():
    response = redirect(url_for("books.list_books"))
    #Eliminamos la cookie que contiene el token
    unset_jwt_cookies(response)
    flash("Sesión cerrada.", "info")
    return response



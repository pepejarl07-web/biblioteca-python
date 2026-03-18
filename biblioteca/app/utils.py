from functools import wraps # herramienta para prreservar la informacion de la funcion original
from flask import redirect, url_for, flash #redirect-> redirige  a otra url *-* url_for -> genera urls a partir de rutas *-* flash -> muestra msgs al usuario
from flask_jwt_extended import verify_jwt_in_request # verifica que la solicitud tiene un token valido

def login_required(f): #recibe la funcion f para definirla
    @wraps(f) # encapsula xa conservar metadatos
    def decorated_function(*args, **kwargs): #funcion para envolver datos que se ejecutara en lugar de la funcion original
        try:#*args y **kwargs recogen indefinidos argumentos
            verify_jwt_in_request() #funcion de flask que comprueba si la peticion HTTP incluye un token válido
            return f(*args, **kwargs) # si no hay errores llama a f con los argumentos que recibió
        except:#lanza una excepcion si el token es invalido o es nulo
            flash("Debes iniciar sesión para acceder a esta página.", "warning")
            return redirect(url_for("auth.login"))#redirige al usuario a la pagina de login para que vuelva a autenticarse
    return decorated_function #devuelve la funcion

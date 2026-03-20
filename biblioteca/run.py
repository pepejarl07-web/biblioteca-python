from flask import Flask, request as flask_request
from app.routes import bp
from app.auth_routes import auth_bp
from flask_jwt_extended import JWTManager, decode_token

def create_app():

    app = Flask(__name__, template_folder="templates", static_folder="static") # crea una instancia de la aplicacion Flask

    #configuracion jwt
    app.secret_key = "claveflash" # CLAVE PARA FLASH
    app.config["JWT_SECRET_KEY"] = "clavejwt" #CLAVE PARA JWT
    app.config["JWT_TOKEN_LOCATION"] = ["cookie"]
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False

    JWTManager(app)

    @app.context_processor # ejecuta auomaticamente las peticiones
    def inject_user_info():
        def current_user_role():
            token_cookie = flask_request.cookies.get("access_token_cookie")# lee la cookie y la guarda
            if not token_cookie: #si no existe, el usuario no ha iniciado sesión
                return None
            try:
                data = decode_token(token_cookie)
                return data.get("role", "user")
            except Exception:
                return None
        def is_logged_in():
            return current_user_role() is not None

        return dict(current_user_role=current_user_role, is_logged_in = is_logged_in)


##En resumen, el flujo completo es:
        ##
##Usuario hace una petición
        ##↓
##Flask ejecuta inject_user_info()
                ##↓
##Lee la cookie JWT → extrae el rol
                    ##↓
##Inyecta is_logged_in() y current_user_role() en Jinja
                        ##↓
##base.html muestra u oculta botones según el resultado

    app.register_blueprint(bp) #rutas de libros
    app.register_blueprint(auth_bp) # rutas de auth


    return app # static_folder, lo mismo.. app.register registra el blueprint que contiene todas las rutas relaccionadas con libros.
    # hace que las rutas definidas en bp pasen a formar parte de la apicacion y finalmente devuelve la app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)



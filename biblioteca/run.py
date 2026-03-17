from flask import Flask
from app.routes import bp

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static") # crea una instancia de la aplicacion Flask
    app.register_blueprint(bp) #__name__ es el nombre del moduclo actual, template_folder indica q las plantillas html estan en la carpeta templates
    return app # static_folder, lo mismo.. app.register registra el blueprint que contiene todas las rutas relaccionadas con libros.
    # hace que las rutas definidas en bp pasen a formar parte de la apicacion y finalmente devuelve la app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)



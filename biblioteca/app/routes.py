from flask import Blueprint, render_template, request, redirect, url_for
from app.database import books_collection
from app.models import validate_book
from bson import ObjectId
import math

bp = Blueprint('books',__name__)

#listar libro con paginación
@bp.route("/books")
def list_books ():
    page = int(request.args.get("page",1)) #pagina actual
    per_page = 5  #libros por pagina
    skip = (page - 1) * per_page #documentos a saltar

    #query de busqueda
    query = {}
    titulo = request.args.get("titulo")
    autor = request.args.get("autor")
    genero = request.args.get("genero")

    if titulo:
        query["titulo"] = {"$regex":titulo, "$options":"i"} #simplemente se señala que la query hacia mongo sea case insensitive
    if autor:
        query["autor"] = {"$regex":autor, "$options": "i"}
    if genero:
        query["genero"] = {"$regex":genero, "$options": "i"}

    total = books_collection.count_documents(query)
    libros = books_collection.find(query).skip(skip).limit(per_page) # devuelve los libros que contengan por ejemplo "quijote"

    return render_template("books/list.html",
                           libros=libros,
                           page = page,
                           total_pages = math.ceil(total / per_page),
                           per_page = per_page,
                           filtros = {"titulo":titulo, "autor":autor, "genero":genero})

#ver detalle de un libro
@bp.route("/books/<id>")
def detail_book(id):
    libro = books_collection.find_one({"_id":ObjectId(id)})
    if not libro:
        return "Libro no encontrado", 404
    return render_template("books/detail.html", libro=libro) #render_template es una funcion de flask:
                                                                        #Busca, procesa la plantilla y genera una cadena de HTML con el resultado
                                                                        #Devulve un objeto RESPONSE que flask enviará al navegador (si existe)
                                                                        #(si no existe) retorna el 404

#Crear libro con get y post
@bp.route("/books/create", methods=["GET","POST"])
def create_book():
    if request.method == "POST":
        data = request.form.to_dict()
        errors = validate_book(data)
        if errors:
            return render_template("books/create.html", errors=errors, data=data)
        #insert en mongodb
        books_collection.insert_one(data)
        return redirect(url_for("books.list_books"))
    return render_template("books/create.html", errors={}, data={})

#Editar libro (GET y POST)
@bp.route("/books/edit/<id>", methods = ["GET", "POST"])
def edit_book(id):
    libro = books_collection.find_one({"_id":ObjectId(id)})
    if not libro:
        return "Libro no encontrado", 404

    if request.method == "POST":
        data = request.form.to_dict()
        errors = validate_book(data)
        if errors:
            return render_template("books/edit.html",errors=errors, libro=libro, id=id)
        #actualizar libro
        books_collection.update_one({"_id":ObjectId(id)}, {"$set":data})
        return redirect(url_for("books.list_books"))
    return render_template("books/edit.html",libro=libro, errors={}, id=id)

#Eliminar libro
@bp.route("/books/delete/<id>", methods=["POST"])
def delete_book(id):
    books_collection.delete_one({"_id":ObjectId(id)})
    return redirect(url_for("books.list_books"))






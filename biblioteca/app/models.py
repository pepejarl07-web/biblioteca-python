from datetime import datetime


def validate_book(data):
    errors = {}
    # campos req
    if not data.get('titulo'):
        errors['titulo'] = "El titulo es obligatorio."
    if not data.get("autor"):
        errors["autor"] = "el autor es obligatorio."
    if not data.get("genero"):
        errors["genero"] = "el genero es obligatorio."

    año = data.get("año")
    if not año:
        errors["año"] = "El año es obligatorio"
    else:
        try:
            año_int = int(año)
            current_year = datetime.now().year
            if año_int <= 0 or año_int > current_year:
                errors["año"] = f"El año tiene que ser un numero positivo y no mayor al actual {current_year}."
        except ValueError:
            errors['año'] = "El año debe ser un numero entero"
    return errors
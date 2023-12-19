from flask import render_template


def error_404(e):
    kwargs = {
        "titulo": "Error 404",
        "nombre_error": "Error 404: Página no encontrada",
        "descripcion_error": "La URL a la que quiere acceder no existe"
    }
    return render_template("error.html", **kwargs), 404


def error_401(e):
    kwargs = {
        "titulo": "Error 401",
        "nombre_error": "Error 401: Falta de credenciales",
        "descripcion_error": "No tiene las credenciales necesarias para acceder a esta URL"
    }
    return render_template("error.html", **kwargs), 401

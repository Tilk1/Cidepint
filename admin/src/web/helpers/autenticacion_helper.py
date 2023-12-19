from flask import session, abort, render_template, flash
from functools import wraps


def esta_auntenticado(session):
    return session.get("usuario") is not None


def inicio_sesion_requerido(f):
    @wraps(f)
    def funcion_decorada(*args, **kwargs):
        if not esta_auntenticado(session):
            return abort(401)
        return f(*args, **kwargs)
    return funcion_decorada


def sesion_activa(f):
    @wraps(f)
    def funcion_decoradora(*args, **kwargs):
        if esta_auntenticado(session):
            flash("Ya tiene una sesión activa en su navegador", "warning")
            return render_template("home.html")
        return f(*args, **kwargs)
    return funcion_decoradora
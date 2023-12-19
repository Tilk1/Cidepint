from functools import wraps
from flask import session, flash, redirect, url_for
from core.models.usuario import Usuario
from src.core.models.solicitud_servicio import SolicitudServicio


def tiene_permiso(**params):
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            usuario = Usuario.buscar_usuario_por_correo(session.get("usuario"))
            if usuario.saber_si_es_super_usuario():
                return f(*args, **kwargs)
            if len(params) != 0:
                lista_roles = usuario.obtener_roles_en_institucion(kwargs.get("id_inst"))
                lista_permisos = []
                for rol in lista_roles:
                    lista_permisos.extend(rol.obtener_permisos())
                nombres_permisos = [permiso.nombre for permiso in lista_permisos]
                for permiso in params.get("permisos_requeridos"):
                    if not (permiso in nombres_permisos):
                        flash("No tiene permisos para acceder a esta seccion", "danger")
                        return redirect(url_for('index.home'))
                return f(*args, **kwargs)
            flash("No tiene permisos para acceder a esta seccion", "danger")
            return redirect(url_for('index.home'))
        return wrapper
    return decorador


def tiene_permiso_front(**kwargs):
    usuario = Usuario.buscar_usuario_por_correo(session.get("usuario"))
    if usuario.saber_si_es_super_usuario():
        return True
    if len(kwargs) != 0:
        lista_roles = usuario.obtener_roles_en_institucion(kwargs.get("id_inst"))
        lista_permisos = []
        for rol in lista_roles:
            lista_permisos.extend(rol.obtener_permisos())
        nombres_permisos = [permiso.nombre for permiso in lista_permisos]
        for permiso in kwargs.get("permisos_requeridos"):
            if not (permiso in nombres_permisos):
                return False
        return True
    return False


def tiene_permiso_solicitud(**params):
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            usuario = Usuario.buscar_usuario_por_correo(session.get("usuario"))
            if usuario.saber_si_es_super_usuario():
                return f(*args, **kwargs)
            if len(params) != 0:
                solicitud = SolicitudServicio.listar(kwargs.get("id"))
                if solicitud is None:
                    flash("No existe ese numero de solicitud", "danger")
                    return redirect(url_for('index.home'))
                servicio = solicitud.obtener_servicio()
                id_inst = servicio.obtener_institucion_id()
                lista_roles = usuario.obtener_roles_en_institucion(id_inst)
                lista_permisos = []
                for rol in lista_roles:
                    lista_permisos.extend(rol.obtener_permisos())
                nombres_permisos = [permiso.nombre for permiso in lista_permisos]
                for permiso in params.get("permisos_requeridos"):
                    if not (permiso in nombres_permisos):
                        flash("No tiene permisos para acceder a esta seccion", "danger")
                        return redirect(url_for('index.home'))
                return f(*args, **kwargs)
            flash("No tiene permisos para acceder a esta seccion", "danger")
            return redirect(url_for('index.home'))
        return wrapper
    return decorador

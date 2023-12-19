from src.core.models.usuario import Usuario
from flask import request, g
from flask import render_template
from src.core.models.configuracion import Configuracion
from flask import session
from src.web.helpers.autenticacion_helper import esta_auntenticado


def verificar_sitio_habilitado():
    ruta_actual = request.path
    RUTAS_PERMITIDAS = ['/auth', '/configuracion']
    if ruta_actual in RUTAS_PERMITIDAS:
        return
    if any(ruta_actual.startswith(prefijo) for prefijo in RUTAS_PERMITIDAS):
        return
    if esta_auntenticado(session):
        usuario = Usuario.buscar_usuario_por_correo(session.get("usuario"))
        if usuario.saber_si_es_super_usuario():
            return
    if not Configuracion.get_sitio_habilitado():
        kwargs = {
            "titulo": "Sitio deshabilitado",
            "nombre_error": "El sitio esta en mantenimiento",
            "descripcion_error": Configuracion.get_mensaje_mantenimiento()
            }
        return render_template("error.html", **kwargs), 404
    g.skip_site_verification = True

from flask import Blueprint, render_template, request, flash
from flask import redirect, url_for, session
from src.core.models.usuario import Usuario
from src.core.models.token import Token
from src.web.utils.validadores import ValidarPreRegistro, ValidarRegistro
from src.web.utils.validadores import ValidarRegistroGoogle

from src.core import mail
from src.web.helpers.autenticacion_helper import sesion_activa
from src.core.oauth_google import oauth


autenticacion_bp = Blueprint("autenticacion", __name__, url_prefix="/auth")


# ----------------------------- Inicio de sesion -----------------------------

@autenticacion_bp.get("/")
@sesion_activa
def iniciar_sesion():
    return render_template("usuario/iniciar_sesion.html")


@autenticacion_bp.post("/autenticar")
@sesion_activa
def autenticarse():
    """Inicia la sesion del usuario"""
    params = request.form
    correo = params["correo"]
    contraseña = params["contraseña"]
    usuario = Usuario.buscar_usuario_por_correo(correo)
    if not usuario:
        flash("Correo electronico o contraseña incorrecta", "danger")
        return render_template("usuario/iniciar_sesion.html")
    if not usuario.obtener_estado():
        flash("Usted ha sido bloqueado. Hable con el administrador", "danger")
        return render_template("usuario/iniciar_sesion.html")
    if usuario.es_cuenta_google:
        flash("Debe iniciar sesion con google", "warning")
        return render_template("usuario/iniciar_sesion.html")
    if usuario.contraseña is None:
        flash("Debe terminar el registro antes de iniciar sesion", "warning")
        return render_template("usuario/iniciar_sesion.html")
    if not Usuario.chequear_contraseña(usuario.contraseña, contraseña):
        flash("Correo electronico o contraseña incorrecta", "danger")
        return render_template("usuario/iniciar_sesion.html")
    session["usuario"] = usuario.correo
    session["mis_instituciones"] = usuario.obtener_instituciones()
    flash("Sesion iniciada con exito", "success")
    return redirect(url_for("index.home"))


@autenticacion_bp.route("/autenticacion-google")
def autenticacion_google():
    redirect_uri = url_for('autenticacion.datos_autenticacion', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@autenticacion_bp.route("/autenticacion-google/callback")
def datos_autenticacion():
    token = oauth.google.authorize_access_token()
    info_usuario = token["userinfo"]
    usuario = Usuario.buscar_usuario_por_correo(info_usuario.email)
    if not usuario:
        flash("Primero debe registrarse con Google", "danger")
        return render_template("home.html")
    if not usuario.obtener_estado():
        flash("Usted ha sido bloqueado. Hable con el administrador", "danger")
        return render_template("home.html")
    session["usuario"] = usuario.correo
    session["mis_instituciones"] = usuario.obtener_instituciones()
    flash("Sesion iniciada con exito", "success")
    return redirect(url_for("index.home"))


@autenticacion_bp.get("/cerrar-sesion")
def cerrar_sesion():
    """Si hay una sesion activa, la cierra"""
    if session.get("usuario"):
        del session["usuario"]
        session.clear()
        flash("La sesion se cerró con exito", "success")
    else:
        flash("No hay sesion iniciada", "info")
    return redirect(url_for("index.home"))


# ----------------------------- Registro Google -----------------------------


@autenticacion_bp.route("/registro-google")
def registro_google():
    redirect_uri = url_for('autenticacion.datos_registro', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@autenticacion_bp.route("/registro-google/callback")
def datos_registro():
    token = oauth.google.authorize_access_token()
    info_usuario = token["userinfo"]
    usuario = Usuario.buscar_usuario_por_correo(info_usuario.email)
    if usuario is not None:
        flash("Usted ya esta registrado, ya puede iniciar sesión con google", "danger")
        return redirect(url_for("index.home"))
    return render_template("usuario/completar_registro_google.html",
                           info_usuario=info_usuario)


@autenticacion_bp.post("/registro-google/completar-registro")
def completar_registro_google():
    params = request.form
    genero = params["genero"]
    if genero == "O":
        genero_otro = params["genero_otro"]
    else:
        genero_otro = genero
    usr = {
        "correo": params["correo"],
        "nombre": params["nombre"],
        "apellido": params["apellido"],
        "nombre_usuario": params["nombre_usuario"],
        "tipo_documento": params["tipo_documento"],
        "nro_documento": params["nro_documento"],
        "direccion": params["direccion"],
        "genero": genero,
        "genero_otro": genero_otro,
        "telefono": params["telefono"],
        "es_cuenta_google": True,
        "activo": True
    }
    respuesta_validacion = ValidarRegistroGoogle.validate(usr)
    if not respuesta_validacion['is_valid']:
        errores = respuesta_validacion["errores"]
        for error_info in errores.items():
            flash(error_info[1]["mensaje"], error_info[1]["estado"])
        return render_template("usuario/completar_registro_google.html",
                               info_usuario={"email": params["correo"],
                                             "given_name": params["nombre"],
                                             "family_name": params["apellido"]})
    Usuario.crear_usuario_google(usr)
    flash("Usuario creado con exito! Inicie sesion con google", "success")
    return redirect(url_for("index.home"))


# ----------------------------- Registro Correo -----------------------------


@autenticacion_bp.get("/preregistro")
def ver_preregistro():
    return render_template("usuario/preregistro.html")


@autenticacion_bp.post("/preregistro")
def preregistro():
    params = request.form
    genero = params["genero"]
    if genero == "O":
        genero_otro = params["genero_otro"]
    else:
        genero_otro = genero
    usr = {
        "correo": params["correo"],
        "nombre": params["nombre"],
        "apellido": params["apellido"],
        "tipo_documento": params["tipo_documento"],
        "nro_documento": params["nro_documento"],
        "direccion": params["direccion"],
        "genero": genero,
        "genero_otro": genero_otro,
        "telefono": params["telefono"]
    }
    respuesta_validacion = ValidarPreRegistro.validate(usr)
    if not respuesta_validacion['is_valid']:
        errores = respuesta_validacion["errores"]
        for error_info in errores.items():
            flash(error_info[1]["mensaje"], error_info[1]["estado"])
        return redirect(url_for("autenticacion.ver_preregistro"))
    token = Token.generar_token(usr)
    if not mail.mandar_mensaje_registro(usr, token):
        Token.eliminar_token(token)
        return redirect(url_for("autenticacion.ver_preregistro"))
    Usuario.crear_usuario_preregistro(usr)
    flash("Usuario creado con exito. Se le ha enviado un correo a su \
            casilla de mensajes para terminar el registro", "success")
    return redirect(url_for("autenticacion.ver_registrarse"))


@autenticacion_bp.get("/registrarse")
def ver_registrarse():
    return render_template("usuario/registrarse.html")


@autenticacion_bp.post("/registrarse")
def registrarse():
    params = request.form
    usr = {
        "nombre_usuario": params["nombre_usuario"],
        "contraseña": params["contraseña"],
        "token": params["token"],
    }
    respuesta_validacion = ValidarRegistro.validate(usr)
    if not respuesta_validacion['is_valid']:
        errores = respuesta_validacion["errores"]
        for error_info in errores.items():
            flash(error_info[1]["mensaje"], error_info[1]["estado"])
        return redirect(url_for("autenticacion.ver_registrarse"))
    usuario = Token.buscar_usuario_con_token(usr["token"])
    Usuario.actualizar_usuario_registro(usuario.correo, usr)
    flash("Registro terminado con exito", "success")
    return redirect(url_for("autenticacion.iniciar_sesion"))

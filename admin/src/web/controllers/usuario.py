from flask import Blueprint, render_template, request, jsonify, abort, flash
from flask import redirect, url_for, session
from src.core.models.usuario import Usuario
from src.web.utils.validadores import ValidarCrearUsuario
from src.web.utils.validadores import ValidarModificarPerfil
from src.web.utils.validadores import ValidarModificarUsuario
from src.web.utils.validadores import ValidarModificarPerfilGoogle
from src.core.models.token import Token
from src.core.models.configuracion import Configuracion
from src.web.helpers.autenticacion_helper import inicio_sesion_requerido
from src.web.helpers.permiso_helper import tiene_permiso

usuario_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@usuario_bp.get("/")
@usuario_bp.get('/<int:pagina>')
@inicio_sesion_requerido
@tiene_permiso()
def mostrar_usuarios(pagina: int = 1):
    config = Configuracion.get_configuracion()
    usuarios_paginados = Usuario.listar_por_pagina(pagina, config.elementos_por_pagina)
    return render_template('usuario/ver_usuarios.html', data=usuarios_paginados, filtro=False)


@usuario_bp.get("/modificar/<int:id>")
@inicio_sesion_requerido
@tiene_permiso()
def mostrar_modificar_usuario(id: int):
    usuario = Usuario.listar(id)
    if usuario is None:
        abort(404)
    return render_template('usuario/modificar_usuario.html', data=usuario)


@usuario_bp.post("/modificar/<int:id>")
@inicio_sesion_requerido
@tiene_permiso()
def modificar_usuario(id: int):
    usuario = Usuario.listar(id)
    if usuario is None:
        return abort(404)
    try:
        params = dict(request.form)
        params['activo'] = (params['activo'] == 'True')
        if usuario.saber_si_es_super_usuario() and not params['activo']:
            flash("No se puede inactivar a un super-administrador", "warning")
            return redirect(url_for('usuarios.mostrar_modificar_usuario', id=id))
        if params["genero"] == "O":
            params["genero_otro"] = params["genero_otro"]
        else:
            params["genero_otro"] = params["genero"]
        usr = {
            "nombre_usuario": params['nombre_usuario'],
            "nombre": params['nombre'],
            "apellido": params['apellido'],
            "activo": params["activo"],
            "tipo_documento": params["tipo_documento"],
            "nro_documento": params["nro_documento"],
            "direccion": params["direccion"],
            "genero": params["genero"],
            "genero_otro": params["genero_otro"],
            "telefono": params["telefono"]
        }
        respuesta_validacion = ValidarModificarUsuario.validate(usr)
        if not respuesta_validacion['is_valid']:
            errores = respuesta_validacion["errores"]
            for error_info in errores.items():
                flash(error_info[1]["mensaje"], error_info[1]["estado"])
            return redirect(url_for('usuarios.mostrar_modificar_usuario', id=id))
        usuario_buscado = Usuario.buscar_usuario_por_nombre_usuario(params['nombre_usuario'])
        if usuario_buscado is not None and usuario_buscado.id != usuario.id:
            flash("Este nombre de usuario ya esta en uso", "danger")
            return redirect(url_for('usuarios.mostrar_modificar_usuario', id=id))
        usuario.modificar(**params)
    except Exception as e:
        flash("No se puede modificar el usuario: " + str(e), "danger")
        return redirect(url_for('usuarios.mostrar_usuarios'))
    else:
        flash("Usuario modificado con exito", "success")
        return redirect(url_for('usuarios.mostrar_modificar_usuario', id=id))


@usuario_bp.get("/eliminar/<int:id>")
@inicio_sesion_requerido
@tiene_permiso()
def mostrar_eliminar_usuario(id: int):
    usuario = Usuario.listar(id)
    if usuario is None:
        abort(404)
    return render_template('usuario/eliminar_usuario.html', data=usuario)


@usuario_bp.post("/eliminar/<int:id>")
@inicio_sesion_requerido
@tiene_permiso()
def eliminar_usuario(id: int):
    try:
        usuario = Usuario.listar(id)
        if usuario.saber_si_es_super_usuario():
            flash("No se puede eliminar a un super-administrador", "warning")
            return redirect(url_for('usuarios.mostrar_usuarios'))
        Token.eliminar_token_con_correo(usuario.correo)
        Usuario.eliminar(usuario)
    except Exception as e:
        flash("No se puede eliminar el usuario: " + str(e), "danger")
    else:
        flash("Usuario eliminado con exito", "success")
    finally:
        return redirect(url_for('usuarios.mostrar_usuarios'))


@usuario_bp.get("/buscar/")
@inicio_sesion_requerido
@tiene_permiso()
def mostrar_buscar_usuario():
    config = Configuracion.get_configuracion()
    pagina = int(request.args.get('pagina'))
    palabra = request.args.get('palabra')
    estado = request.args.get('activoradio')
    usr_filt_pag = Usuario.listar_filtrado(pagina, config.elementos_por_pagina,
                                           palabra, estado)
    return render_template("usuario/ver_usuarios.html", data=usr_filt_pag,
                           filtro=True, palabra=palabra, estado=estado)


@usuario_bp.get("/crear-usuario")
@inicio_sesion_requerido
@tiene_permiso()
def mostrar_crear_usuario():
    return render_template('usuario/crear_usuario.html')


@usuario_bp.post("/crear-usuario")
@inicio_sesion_requerido
@tiene_permiso()
def crear_usuario():
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
        "telefono": params["telefono"],
        "contraseña": params["contraseña"],
        "nombre_usuario": params["nombre_usuario"],
        "activo": True,
        "es_super_admin": False
    }
    respuesta_validacion = ValidarCrearUsuario.validate(usr)
    if respuesta_validacion['is_valid']:
        Usuario.crear_usuario(usr)
        flash("Usuario creado con exito", "success")
        return redirect(url_for("usuarios.mostrar_crear_usuario"))
    else:
        errores = respuesta_validacion["errores"]
        for error_info in errores.items():
            flash(error_info[1]["mensaje"], error_info[1]["estado"])
        return redirect(url_for("usuarios.mostrar_crear_usuario"))


@usuario_bp.get("/modificar-perfil")
@inicio_sesion_requerido
def mostrar_modificar_perfil():
    correo = session.get("usuario")
    usuario = Usuario.buscar_usuario_por_correo(correo)
    return render_template("usuario/modificar_perfil.html", data=usuario)


@usuario_bp.post("/modificar-perfil")
@inicio_sesion_requerido
def modificar_perfil():
    correo = session.get("usuario")
    usuario = Usuario.buscar_usuario_por_correo(correo)
    params = request.form
    nueva_contraseña = params["nueva_contraseña"]
    chequeo_contraseña = params["chequeo_contraseña"]
    genero = params["genero"]
    if genero == "O":
        genero_otro = params["genero_otro"]
    else:
        genero_otro = genero
    if not len(nueva_contraseña):
        contraseña = usuario.contraseña
    else:
        contraseña = nueva_contraseña
    usr = {
        "correo": correo,
        "nombre_usuario": params['nombre_usuario'],
        "nombre": params['nombre'],
        "apellido": params['apellido'],
        "contraseña": contraseña,
        "tipo_documento": params['tipo_documento'],
        "nro_documento": params['nro_documento'],
        "direccion": params['direccion'],
        "genero": genero,
        "genero_otro": genero_otro,
        "telefono": params['telefono'],
    }
    respuesta_validacion = ValidarModificarPerfil.validate(usr)
    if not respuesta_validacion['is_valid']:
        errores = respuesta_validacion["errores"]
        for error_info in errores.items():
            flash(error_info[1]["mensaje"], error_info[1]["estado"])
        return render_template('usuario/modificar_perfil.html', data=usuario)
    if not Usuario.chequear_contraseña(usuario.contraseña, chequeo_contraseña):
        flash("Contraseña incorrecta: no se modificaran sus datos", "warning")
        return render_template('usuario/modificar_perfil.html', data=usuario)
    usuario_buscado = Usuario.buscar_usuario_por_nombre_usuario(params['nombre_usuario'])
    if usuario_buscado is not None and usuario_buscado.id != usuario.id:
        flash("Este nombre de usuario ya esta en uso", "danger")
        return render_template('usuario/modificar_perfil.html', data=usuario)
    Usuario.modificar_perfil(usr)
    flash("Perfil modificado con exito", "success")
    return render_template('usuario/modificar_perfil.html', data=usuario)


@usuario_bp.post("/modificar-perfil-google")
@inicio_sesion_requerido
def modificar_perfil_google():
    correo = session.get("usuario")
    usuario = Usuario.buscar_usuario_por_correo(correo)
    params = request.form
    genero = params["genero"]
    if genero == "O":
        genero_otro = params["genero_otro"]
    else:
        genero_otro = genero
    usr = {
        "correo": correo,
        "nombre_usuario": params['nombre_usuario'],
        "nombre": params['nombre'],
        "apellido": params['apellido'],
        "tipo_documento": params['tipo_documento'],
        "nro_documento": params['nro_documento'],
        "direccion": params['direccion'],
        "genero": genero,
        "genero_otro": genero_otro,
        "telefono": params['telefono'],
    }
    respuesta_validacion = ValidarModificarPerfilGoogle.validate(usr)
    if not respuesta_validacion['is_valid']:
        errores = respuesta_validacion["errores"]
        for error_info in errores.items():
            flash(error_info[1]["mensaje"], error_info[1]["estado"])
        return render_template('usuario/modificar_perfil.html', data=usuario)
    usuario_buscado = Usuario.buscar_usuario_por_nombre_usuario(params['nombre_usuario'])
    if usuario_buscado is not None and usuario_buscado.id != usuario.id:
        flash("Este nombre de usuario ya esta en uso", "danger")
        return render_template('usuario/modificar_perfil.html', data=usuario)
    Usuario.modificar_perfil_google(usr)
    flash("Perfil modificado con exito", "success")
    return render_template('usuario/modificar_perfil.html', data=usuario)


@usuario_bp.post("/eliminar-perfil")
@inicio_sesion_requerido
def eliminiar_perfil():
    params = request.form
    correo = session.get("usuario")
    usuario = Usuario.buscar_usuario_por_correo(correo)
    if usuario.saber_si_es_super_usuario():
        flash("No se puede eliminar a un super-administrador", "warning")
        return render_template('usuario/modificar_perfil.html', data=usuario)
    chequeo_contraseña = params["chequeo_contraseña_eliminar"]
    if not Usuario.chequear_contraseña(usuario.contraseña, chequeo_contraseña):
        flash("Contraseña incorrecta: no se puede eliminar su cuenta", "warning")
        return render_template('usuario/modificar_perfil.html', data=usuario)
    Usuario.eliminar(usuario)
    Token.eliminar_token_con_correo(correo)
    if session.get("usuario"):
        del session["usuario"]
        session.clear()
    flash("Su perfil ha sido eliminado con exito", "success")
    return render_template("home.html")


@usuario_bp.post("/eliminar-perfil-google")
@inicio_sesion_requerido
def eliminiar_perfil_google():
    correo = session.get("usuario")
    usuario = Usuario.buscar_usuario_por_correo(correo)
    if usuario.saber_si_es_super_usuario():
        flash("No se puede eliminar a un super-administrador", "warning")
        return render_template('usuario/modificar_perfil.html', data=usuario)
    Usuario.eliminar(usuario)
    if session.get("usuario"):
        del session["usuario"]
        session.clear()
    flash("Su perfil ha sido eliminado con exito", "success")
    return render_template("home.html")

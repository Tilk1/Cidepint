from flask import Blueprint, render_template, request
from flask import url_for, flash, abort, redirect
from src.core.models.institucion import Institucion
from src.core.models.configuracion import Configuracion
from src.web.helpers.permiso_helper import tiene_permiso
from src.web.helpers.autenticacion_helper import inicio_sesion_requerido
from src.core.models.usuario import Usuario
from flask import session
from src.core.models.rol import Rol


# Crear un Blueprint
instituciones_bp = Blueprint("instituciones", __name__,
                             url_prefix="/instituciones")


@instituciones_bp.route('/')
@instituciones_bp.route('/<int:pagina>')
@inicio_sesion_requerido
@tiene_permiso()
def index(pagina: int = 1):
    if pagina < 1:
        return abort(404)
    elementos_por_pagina = Configuracion.get_elementos_por_pagina()
    instituciones_paginadas = Institucion.listar_por_pagina(pagina, elementos_por_pagina)
    return render_template('instituciones/instituciones.html',
                           data=instituciones_paginadas)


@instituciones_bp.post("/")
@inicio_sesion_requerido
@tiene_permiso()
def acciones():
    institucion = Institucion.listar(request.form.get("id"))
    accion = request.form.get("accion")
    if accion == "modificar":
        return redirect(url_for("instituciones.mostrar_formulario_modificar",
                                id=institucion.id))


@instituciones_bp.get("/eliminar/<int:id>")
@inicio_sesion_requerido
@tiene_permiso()
def mostrar_confirmacion_eliminar(id: int):
    institucion = Institucion.listar(id)
    if institucion is None:
        abort(404)
    return render_template("instituciones/institucion_eliminar.html",
                           data=institucion)


@instituciones_bp.post("/eliminar/<int:id>")
@inicio_sesion_requerido
@tiene_permiso()
def eliminar(id: int):
    try:
        institucion = Institucion.listar(id)
        list(map(lambda servicio: servicio.eliminar(), institucion.servicios))
        institucion.eliminar()
    except Exception as e:
        flash("No se puede eliminar la institucion: " + str(e), "danger")
    else:
        flash("Institucion eliminada con exito", "success")
    finally:
        return redirect(url_for("instituciones.index"))


@instituciones_bp.get("/formulario_crear")
@inicio_sesion_requerido
@tiene_permiso()
def mostrar_formulario():
    return render_template("instituciones/institucion_crear.html")


@instituciones_bp.post("/formulario_crear")
@inicio_sesion_requerido
@tiene_permiso()
def crear():
    try:
        datos_formulario = dict(request.form)
        datos_formulario.pop("Dueño", None)
        datos_formulario["habilitada"] = (datos_formulario["habilitada"] == "True")
        dueño = Usuario.buscar_usuario_por_correo(request.form['Dueño'])
        if dueño is None:
            flash("No existe usuario con ese correo", "danger")
            return redirect(url_for("instituciones.crear"))
        nueva_institucion = Institucion.crear(**datos_formulario)
        nueva_institucion.agregar_integrante(dueño, Rol.obtener_rol("Dueño"))
    except Exception as e:
        flash("No se puede crear la institucion: " + str(e), "danger")
        return redirect(url_for("instituciones.index"))
    else:
        flash("Institucion creada con exito", "success")
        return redirect(url_for("instituciones.index"))


@instituciones_bp.get('/modificar/<int:id>')
@inicio_sesion_requerido
@tiene_permiso()
def mostrar_formulario_modificar(id: int):
    institucion = Institucion.listar(id)
    if institucion is None:
        abort(404)
    return render_template('instituciones/institucion_modificar.html',
                           data=institucion)


@instituciones_bp.post('/modificar/<int:id>')
@inicio_sesion_requerido
@tiene_permiso()
def modificar(id: int):
    institucion = Institucion.listar(id)
    if institucion is None:
        return abort(404)
    try:
        datos_formulario = dict(request.form)
        datos_formulario["habilitada"] = (datos_formulario["habilitada"] == "True")
        institucion.modificar(**datos_formulario)
    except Exception as e:
        flash("No se puede modificar la institucion: " + str(e), "danger")
        return redirect(url_for('instituciones.index'))
    else:
        flash("Institucion modificada con exito", "success")
        return redirect(url_for('instituciones.modificar', id=id))


@instituciones_bp.get("/detalle/<int:id_inst>")
@inicio_sesion_requerido
@tiene_permiso(permisos_requeridos=["admin_servicios_index"])
def mostrar_detalle_institucion(id_inst: int):
    institucion = Institucion.listar(id_inst)
    usuario = Usuario.buscar_usuario_por_correo(session.get("usuario"))
    datos_usuario_en_institucion = {}  # utiliza la ternaria
    datos_usuario_en_institucion["rol"] = institucion.obtener_rol_usuario(usuario)
    data = {
        "institucion": institucion,
        "datos_usuario_en_institucion": datos_usuario_en_institucion,
        "usuario": usuario
        }

    if institucion is None:
        abort(404)
    return render_template("instituciones/institucion_detalle.html", data=data)


@instituciones_bp.post("/detalle/<int:id_inst>")
@inicio_sesion_requerido
@tiene_permiso(permisos_requeridos=["admin_usuarios_institucion_create"])
def agregar_integrante(id_inst: int):
    institucion = Institucion.listar(id_inst)
    if institucion is None:
        abort(404)

    nuevo_integrante = Usuario.buscar_usuario_por_correo(request.form['correo'])
    if nuevo_integrante is None:
        flash("No existe el usuario", "danger")
        return redirect(url_for("instituciones.mostrar_detalle_institucion",
                                id_inst=id_inst))

    if institucion.obtener_rol_usuario(nuevo_integrante) is not None:
        flash("El usuario ya es integrante de la institucion", "danger")
        return redirect(url_for("instituciones.mostrar_detalle_institucion",
                                id_inst=id_inst))

    try:
        rol_por_defecto = Rol.obtener_rol("Operador")
        institucion.agregar_integrante(nuevo_integrante, rol_por_defecto)
    except Exception as e:
        flash("No se puede agregar el integrante: " + str(e), "danger")
    else:
        flash("Integrante agregado con exito", "success")
    finally:
        return redirect(url_for("instituciones.mostrar_detalle_institucion",
                                id_inst=id_inst))


@instituciones_bp.get("/detalle/<int:id_inst>/administrar_integrantes/")
@instituciones_bp.get("/detalle/<int:id_inst>/administrar_integrantes/<int:pagina>")
@inicio_sesion_requerido
@tiene_permiso(permisos_requeridos=["admin_usuarios_institucion_index"])
def mostrar_administrar_integrantes(id_inst: int, pagina: int = 1):
    institucion = Institucion.listar(id_inst)
    config = Configuracion.listar(1)
    integrantes = institucion.obtener_integrantes_paginados(pagina, config.elementos_por_pagina)
    lista_con_roles = []
    for integrante in integrantes["data"]:
        usuario_info = {
            "integrante": integrante,
            "rol": integrante.obtener_roles_en_institucion(institucion.id)
        }
        lista_con_roles.append(usuario_info)
    integrantes["data"] = lista_con_roles
    return render_template("/instituciones/administrar_integrantes.html",
                           data=integrantes, id_inst=id_inst, filtro=False)


@instituciones_bp.get("/detalle/<int:id_inst>/administrar_integrantes/buscar/")
@inicio_sesion_requerido
@tiene_permiso(permisos_requeridos=["admin_usuarios_institucion_index"])
def mostrar_administrar_integrantes_filtrado(id_inst: int, pagina: int = 1):
    config = Configuracion.listar(1)
    pagina = int(request.args.get('pagina'))
    palabra = request.args.get('palabra')
    estado = request.args.get('activoradio')
    institucion = Institucion.listar(id_inst)
    integrantes_filtrados = institucion.listar_filtrado_integrantes(pagina, config.elementos_por_pagina,
                                           palabra, estado)
    lista_con_roles = []
    for integrante in integrantes_filtrados["data"]:
        usuario_info = {
            "integrante": integrante,
            "rol": integrante.obtener_roles_en_institucion(institucion.id)
        }
        lista_con_roles.append(usuario_info)
    integrantes_filtrados["data"] = lista_con_roles
    return render_template("/instituciones/administrar_integrantes.html",
                           data=integrantes_filtrados, filtro=True,
                           palabra=palabra, estado=estado, id_inst=id_inst)


@instituciones_bp.get("/detalle/<int:id_inst>/expulsar_integrante/<int:id_usuario>")
@inicio_sesion_requerido
@tiene_permiso(permisos_requeridos=["admin_usuarios_institucion_destroy"])
def mostrar_expulsar_integrante(id_inst: int, id_usuario: int):
    usuario = Usuario.listar(id_usuario)
    institucion = Institucion.listar(id_inst)
    if usuario is None:
        flash("Ese usuario no existe en el sistema ", "danger")
        return redirect(url_for("instituciones.mostrar_administrar_integrantes",
                                id_inst=id_inst, pagina=1))
    if not institucion.usuario_es_integrante(usuario):
        flash("Ese usuario no es parte de la institucion", "danger")
        return redirect(url_for("instituciones.mostrar_administrar_integrantes",
                                id_inst=id_inst, pagina=1))
    return render_template("instituciones/expulsar_integrante.html", 
                           id_inst=id_inst, data=usuario)


@instituciones_bp.post("/detalle/<int:id_inst>/expulsar_integrante/<int:id_usuario>")
@inicio_sesion_requerido
@tiene_permiso(permisos_requeridos=["admin_usuarios_institucion_destroy"])
def expulsar_integrante(id_inst: int, id_usuario: int, pagina: int = 1):
    usuario = Usuario.listar(id_usuario)
    institucion = Institucion.listar(id_inst)
    if usuario is None:
        flash("El usuario ingresado no se encuentra registrado", "danger")
        return redirect(url_for("instituciones.mostrar_administrar_integrantes",
                                id_inst=id_inst, pagina=1))
    institucion.eliminar_rol_usuario(usuario)
    flash("El integrante ha sido eliminado de la institucion", "success")
    return redirect(url_for("instituciones.mostrar_administrar_integrantes",
                            id_inst=id_inst, pagina=1))


@instituciones_bp.get("/detalle/<int:id_inst>/modificar_rol/<int:id_usuario>")
@inicio_sesion_requerido
@tiene_permiso(permisos_requeridos=["admin_usuarios_institucion_update"])
def mostrar_modificar_rol(id_inst: int, id_usuario: int):
    usuario = Usuario.listar(id_usuario)
    institucion = Institucion.listar(id_inst)
    if usuario is None:
        flash("Ese usuario no existe en el sistema ", "danger")
        return redirect(url_for("instituciones.mostrar_administrar_integrantes",
                                id_inst=id_inst, pagina=1))
    if not institucion.usuario_es_integrante(usuario):
        flash("Ese usuario no es parte de la institucion", "danger")
        return redirect(url_for("instituciones.mostrar_administrar_integrantes",
                                id_inst=id_inst, pagina=1))
    usuario_con_rol = {
            "usuario": usuario,
            "rol": usuario.obtener_roles_en_institucion(institucion.id)
        }
    return render_template("instituciones/modificar_rol.html", id_inst=id_inst,
                           data=usuario_con_rol)


@instituciones_bp.post("/detalle/<int:id_inst>/modificar_rol/<int:id_usuario>")
@inicio_sesion_requerido
@tiene_permiso(permisos_requeridos=["admin_usuarios_institucion_update"])
def modificar_rol(id_inst: int, id_usuario: int):
    usuario = Usuario.listar(id_usuario)
    institucion = Institucion.listar(id_inst)
    if usuario is None:
        flash("El usuario ingresado no se encuentra registrado", "danger")
        return redirect(url_for("instituciones.mostrar_administrar_integrantes",
                                id_inst=id_inst, pagina=1))
    institucion.eliminar_rol_usuario(usuario)
    rol = Rol.obtener_rol(request.form['rol'])
    institucion.agregar_integrante(usuario, rol)
    flash("Se ha cambiado el rol exitosamente", "success")
    return redirect(url_for("instituciones.mostrar_administrar_integrantes",
                            id_inst=id_inst, pagina=1))

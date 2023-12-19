from flask import Blueprint, render_template, request
from flask import redirect, url_for, abort
from flask import flash
from flask import session
from src.core.models.servicio import Servicio
from src.core.models.institucion import Institucion
from src.core.models.usuario import Usuario
from src.core.models.configuracion import Configuracion
from src.web.helpers.permiso_helper import tiene_permiso
from src.web.helpers.autenticacion_helper import inicio_sesion_requerido

servicios_bp = Blueprint('servicios', __name__, url_prefix='/servicios')


@servicios_bp.get('/')
@servicios_bp.get('/<int:pagina>')
@inicio_sesion_requerido
@tiene_permiso()
def index(pagina: int = 1):
    if pagina < 1:
        return abort(404)
    elementos_pagina = Configuracion.get_elementos_por_pagina()
    servicios_paginados = Servicio.listar_por_pagina(pagina, elementos_pagina)
    for servicio in servicios_paginados['data']:  # agrega las instituciones
        institucion = Institucion.listar(servicio['institucion_id']).json()
        servicio['institucion'] = institucion
    return render_template('servicios/ver_servicios.html',
                           data=servicios_paginados, id_inst=0)


@servicios_bp.get('/ver_servicios_institucion/<int:id_inst>')
@servicios_bp.get('/ver_servicios_institucion/<int:id_inst>/<int:pagina>')
@inicio_sesion_requerido
@tiene_permiso(permisos_requeridos=["admin_servicios_index"])
def ver_servicios_institucion(id_inst: int, pagina: int = 1):
    if pagina < 1:
        return abort(404)
    elementos_pagina = Configuracion.get_elementos_por_pagina()
    servicios_paginados = Servicio.paginar_servicios_institucion(
        id_inst, pagina, elementos_pagina)
    return render_template('servicios/ver_servicios.html',
                           data=servicios_paginados, id_inst=id_inst)


@servicios_bp.route('/alta_servicio/<int:id_inst>')
@inicio_sesion_requerido
@tiene_permiso(permisos_requeridos=["admin_servicios_create"])
def alta_servicio(id_inst: int):
    usuario = Usuario.buscar_usuario_por_correo(session.get("usuario"))
    instituciones = []
    if (usuario.saber_si_es_super_usuario()) and (id_inst == 0):
        instituciones = Institucion.listar_todos()
    else:
        instituciones.append(Institucion.listar(id_inst))
    return render_template('servicios/alta_servicio.html',
                           data=instituciones, id_inst=id_inst)


@servicios_bp.post('/alta_servicio/<int:id_inst>')
@inicio_sesion_requerido
@tiene_permiso(permisos_requeridos=["admin_servicios_create"])
def crear_servicio(id_inst: int):
    try:
        admin = False
        if (id_inst == 0):
            admin = True
        usuario = Usuario.buscar_usuario_por_correo(session.get("usuario"))
        if (usuario.saber_si_es_super_usuario()):
            id_inst = request.form['institucion']
        habilitado = request.form['habilitado']
        opcion = (habilitado == "True")
        Servicio.crear(
            nombre=request.form['nombre'],
            descripcion=request.form['descripcion'],
            tipo=request.form['tipo'],
            palabras_claves=request.form['palabras_claves'],
            habilitado=opcion,
            institucion_id=id_inst
            )
    except Exception as e:
        flash('Error al crear el servicios' + str(e), 'danger')
    else:
        flash('Servicio creado correctamente', 'success')
    if (usuario.saber_si_es_super_usuario()) and (admin):
        return redirect(url_for("servicios.index"))
    return redirect(url_for("servicios.ver_servicios_institucion",
                            id_inst=id_inst))


@servicios_bp.get('/editar_servicio/<int:id_inst>/<int:id>')
@inicio_sesion_requerido
@tiene_permiso(permisos_requeridos=["admin_servicios_update"])
def ver_servicio(id_inst: int, id: int):
    servicio = Servicio.listar(id)
    usuario = Usuario.buscar_usuario_por_correo(session.get("usuario"))
    admin = usuario.saber_si_es_super_usuario()
    return render_template('servicios/editar_servicio.html',
                           servicio=servicio, id_inst=id_inst, admin=admin)


@servicios_bp.post('/editar_servicio/<int:id_inst>/<int:id>')
@inicio_sesion_requerido
@tiene_permiso(permisos_requeridos=["admin_servicios_update"])
def editar_servicio(id_inst: int, id: int):
    servicio = Servicio.listar(id)
    habilitado = request.form['habilitado']
    opcion = (habilitado == 'True')
    servicio.modificar(
        nombre=request.form['nombre'],
        descripcion=request.form['descripcion'],
        tipo=request.form['tipo'],
        palabras_claves=request.form['palabras_clave'],
        habilitado=opcion
        )
    usuario = Usuario.buscar_usuario_por_correo(session.get("usuario"))
    flash('Servicio actualizado correctamente', 'success')
    if (usuario.saber_si_es_super_usuario()) and (id_inst == 0):
        return redirect(url_for("servicios.index"))
    return redirect(url_for("servicios.ver_servicios_institucion",
                            id_inst=id_inst))


@servicios_bp.route('/eliminar_servicio/<int:id_inst>/<int:id>')
@inicio_sesion_requerido
@tiene_permiso(permisos_requeridos=["admin_servicios_destroy"])
def eliminar_servicio(id_inst: int, id: int):
    servicio = Servicio.listar(id)
    return render_template('servicios/eliminar_servicio.html',
                           data=servicio, id_inst=id_inst)


@servicios_bp.post('/eliminar_servicio/<int:id_inst>/<int:id>')
@inicio_sesion_requerido
@tiene_permiso(permisos_requeridos=["admin_servicios_destroy"])
def borrar_servicio(id_inst: int, id: int):
    servicio = Servicio.listar(id)
    usuario = Usuario.buscar_usuario_por_correo(session.get("usuario"))
    if servicio is None:
        flash('Servicio no encontrado', 'danger')
        return redirect(url_for("servicios.index"))
    try:
        servicio.eliminar()
        flash('Servicio eliminado correctamente', 'success')
    except Exception as e:
        flash('Error al eliminar servicio'+e, 'danger')
    finally:
        if (usuario.saber_si_es_super_usuario()) and (id_inst == 0):
            return redirect(url_for("servicios.index"))
        return redirect(url_for("servicios.ver_servicios_institucion",
                                id_inst=id_inst))

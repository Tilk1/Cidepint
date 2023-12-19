from flask import Blueprint, render_template, request, jsonify
from flask import url_for, flash, abort, redirect, session
from src.core.models.solicitud_servicio import SolicitudServicio
from src.core.models.solicitud_servicio import EstadoEnum
from src.core.models.usuario import Usuario
from src.core.models.servicio import Servicio
from src.core.models.servicio import Tipos as tipos_servicio
from src.core.models.configuracion import Configuracion
from src.core.models.solicitud_servicio import EstadoEnum as estados_solicitud
from src.core.models.institucion import Institucion
from src.core.models.nota_solicitud import NotaSolicitud
from src.web.helpers.permiso_helper import tiene_permiso, tiene_permiso_front
from src.web.helpers.permiso_helper import tiene_permiso_solicitud
from src.web.helpers.autenticacion_helper import inicio_sesion_requerido

solicitud_servicio_bp = Blueprint('solicitud_servicio', __name__,
                                  url_prefix='/servicios/solicitudes')


@solicitud_servicio_bp.route('/')
@solicitud_servicio_bp.route('/<int:pagina>')
@inicio_sesion_requerido
@tiene_permiso()
def index(pagina: int = 1):
    if pagina < 1:
        return abort(404)
    elementos_por_pagina = Configuracion.get_elementos_por_pagina()
    solicitudes_paginadas = SolicitudServicio.listar_por_pagina(pagina, elementos_por_pagina)
    for solicitud in solicitudes_paginadas['data']:  # agrega datos adicionales
        solicitud["solicitante"] = Usuario.listar(solicitud['usuario_id'])
        solicitud["servicio_solicitado"] = Servicio.listar(solicitud['servicio_id'])
    enums_estados = [{'value': member.value, 'name': member.name} for member in estados_solicitud]
    enums_tipos = [{'value': member.value, 'name': member.name} for member in tipos_servicio]
    return render_template('servicios/ver_solicitudes.html',
                           data=solicitudes_paginadas,
                           enums_estados=enums_estados,
                           enums_tipos=enums_tipos)


@solicitud_servicio_bp.get('/modificar/<int:id>')
@inicio_sesion_requerido
@tiene_permiso_solicitud(permisos_requeridos=["solicitud_servicios_show"])
def ver_detalle_solicitud(id: int):
    solicitud = SolicitudServicio.listar(id)
    if solicitud is None:
        abort(404)
    solicitante = Usuario.listar(solicitud.usuario_id)
    servicio_solicitado = Servicio.listar(solicitud.servicio_id)
    notas_de_solicitud = solicitud.obtener_notas()

    notas_de_solicitud_list = []
    for nota in notas_de_solicitud:
        escrito_por = Usuario.listar(nota.usuario_id).nombre_usuario
        nota_dict = {
            "texto": nota.nota,
            "creado_el": nota.creado_el,
            "actualizado_el": nota.actualizado_el,
            "escrito_por": escrito_por
        }
        notas_de_solicitud_list.append(nota_dict)

    data = {
        "solicitud": solicitud.json(),
        "solicitante": solicitante.json(),
        "servicio_solicitado": servicio_solicitado.json(),
        "notas": notas_de_solicitud_list
        }
    enums_estados = [{'value': member.value, 'name': member.name}
                     for member in estados_solicitud]
    return render_template('servicios/editar_solicitud.html', data=data,
                           enums_estados=enums_estados)


@solicitud_servicio_bp.post('/modificar/<int:id>')
@inicio_sesion_requerido
@tiene_permiso_solicitud(permisos_requeridos=["solicitud_servicios_update"])
def actualizar(id: int):
    solicitud = SolicitudServicio.listar(id)
    if solicitud is None:
        abort(404)
    try:
        datos_formulario = dict(request.form)
        datos_formulario["estado"] = EstadoEnum(request.form['estado'])
        usuario = Usuario.buscar_usuario_por_correo(session.get("usuario"))
        if datos_formulario["respuesta_al_cliente"] != "":
            NotaSolicitud.crear(nota=datos_formulario["respuesta_al_cliente"],
                                solicitud_id=id, usuario_id=usuario.id)
        solicitud.modificar(**datos_formulario)
        solicitud.actualizar_cierre_solicitud()
    except Exception as e:
        flash('Solicitud fallida: ' + str(e), 'danger')
        return redirect(url_for('solicitud_servicio.index'))
    else:
        flash('Solicitud actualizada correctamente', 'success')
        return redirect(url_for('solicitud_servicio.ver_detalle_solicitud', id=id))


@solicitud_servicio_bp.get("/buscar/")
@inicio_sesion_requerido
def mostrar_buscar_solicitud():
    institucion_id = request.args.get('institucion_id')
    if not tiene_permiso_front(id_inst=institucion_id, permisos_requeridos=["solicitud_servicios_index"]):
        flash("No tiene permisos para acceder a esta seccion", "danger")
        return redirect(url_for('index.home'))
    elementos_por_pagina = Configuracion.get_elementos_por_pagina()
    pagina = int(request.args.get('pagina'))
    solicitante = request.args.get('solicitante')
    tipo = request.args.get('tipo')
    estado = request.args.get('estado')
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')
    solicitudes_filtradas = SolicitudServicio.listar_filtrado(solicitante,
                                                            tipo,
                                                            estado,
                                                            desde,
                                                            hasta,
                                                            institucion_id)
    solicitudes_paginadas = SolicitudServicio.paginar(
        solicitudes_filtradas, pagina, elementos_por_pagina)

    for solicitud in solicitudes_paginadas['data']:  # agrega datos adicionales
        solicitud["solicitante"] = Usuario.listar(solicitud['usuario_id'])
        solicitud["servicio_solicitado"] = Servicio.listar(solicitud['servicio_id'])

    enums_estados = [{'value': member.value, 'name': member.name} for member in estados_solicitud]
    enums_tipos = [{'value': member.value, 'name': member.name} for member in tipos_servicio]
    return render_template("servicios/ver_solicitudes.html",
                        data=solicitudes_paginadas,
                        filtro=True, solicitante=solicitante, estado=estado,
                        desde=desde, hasta=hasta, tipo=tipo,
                        enums_estados=enums_estados,
                        enums_tipos=enums_tipos,
                            institucion_id=institucion_id)


@solicitud_servicio_bp.route('/')
@solicitud_servicio_bp.route('/institucion/<int:id_inst>/<int:pagina>')
@inicio_sesion_requerido
@tiene_permiso(permisos_requeridos=["solicitud_servicios_index"])
def mostrar_solicitudes_de_institucion(id_inst: int, pagina: int = 1):
    institucion = Institucion.listar(id_inst)
    if pagina < 1 or institucion is None:
        return abort(404)
    servicios = institucion.obtener_servicios()
    solicitudes = []
    for servicio in servicios:
        solicitudes.extend(servicio.obtener_solicitudes())
    elementos_por_pagina = Configuracion.get_elementos_por_pagina()
    solicitudes_paginadas = SolicitudServicio.paginar(solicitudes, pagina, elementos_por_pagina)
    for solicitud in solicitudes_paginadas['data']:  # agrega datos adicionales
        solicitud["solicitante"] = Usuario.listar(solicitud['usuario_id'])
        solicitud["servicio_solicitado"] = Servicio.listar(solicitud['servicio_id'])
    enums_estados = [{'value': member.value, 'name': member.name} for member in estados_solicitud]
    enums_tipos = [{'value': member.value, 'name': member.name} for member in tipos_servicio]
    return render_template('servicios/ver_solicitudes.html',
                            data=solicitudes_paginadas,
                            enums_estados=enums_estados,
                            enums_tipos=enums_tipos,
                            institucion_id=id_inst)

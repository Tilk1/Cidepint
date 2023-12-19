from datetime import timedelta
from functools import wraps
import json
from src.web.utils.autenticacion import Autenticacion
from src.core.models.configuracion import Configuracion
from src.core.models.nota_solicitud import NotaSolicitud
from src.core.models.usuario import Usuario
from flask import Blueprint, jsonify, request, abort
from src.core.models.institucion import Institucion
from src.core.models.servicio import Servicio
from src.core.models.solicitud_servicio import EstadoEnum, SolicitudServicio
from flask_jwt_extended import jwt_required
from geopy.geocoders import Nominatim
from src.web.utils.validadores import ValidarRegistroCorreoAPI
from src.web.utils.validadores import ValidarRegistroGoogleAPI
from src.web.utils.validadores import ValidarCompletarDatosGoogleAPI

api_bp = Blueprint("api", __name__, url_prefix="/api")
atributos_excluidos_servicios = ["creado_el", "actualizado_el"]
atributos_excluidos_instituciones = ["id", "palabras_clave", "creado_el", "actualizado_el"]


def caracteres_validos(func):
    """Verifica que los caracteres ingresados en los parámetros
        page y per_page sean dígitos
    Args:
        func (function): función a decorar
    Returns:
        func : función decorada
    """
    @wraps(func)
    def decorador(*args, **kwargs):
        if (not (str(request.args.get('page', 1)).isdigit())
           or not (str(request.args.get('per_page', Configuracion.get_elementos_por_pagina())).isdigit())):
            error = {"error": 'Parámetros inválidos'}
            return jsonify(error), 400
        return func(*args, **kwargs)
    return decorador


@api_bp.route('/institutions', methods=['GET'])
@caracteres_validos
def obtener_instituciones():
    """Lista las instituciones en formato json
    Returns:
        institucion: lista de instituciones
    """
    pagina = int(request.args.get('page', 1))
    por_pagina = int(request.args.get('per_page', Configuracion.get_elementos_por_pagina()))
    return Institucion.listar_por_pagina(pagina, por_pagina, atributos_excluidos_instituciones)


@api_bp.route('/services/search', methods=['GET'])
@jwt_required()
@caracteres_validos
def obtener_servicios_buscados():
    """Lista los servicios buscados por término de búsqueda y
    por su tipo en formato json
    Returns:
        lista: lista con servicios buscados
    """
    pagina = int(request.args.get('page', 1))
    por_pagina = int(request.args.get('per_page', Configuracion.get_elementos_por_pagina()))
    tipo = request.args.get('type', None)
    q = str(request.args.get('q'))
    serv = Servicio.listar_por_pagina_y_tipo(tipo, q, pagina, por_pagina,
                                             atributos_excluidos_servicios)
    serv['data'] = json_api(serv)
    return serv


@api_bp.route('/services/<int:id>', methods=['GET'])
def detalle_servicio(id):
    """Obtiene el detalle de un servicio específico
       en formato json
    Args:
        id (int): id del servicio
    Returns:
        serv : información del servicio
    """
    if str(id).isdigit():
        serv = Servicio.obtener_detalle_de_servicio(id, atributos_excluidos_servicios)
        if serv != {}:
            serv = json_servicio(serv)
            return serv
        return abort(404)
    return jsonify({"error": 'Parámetros inválidos'}), 400


@api_bp.route('/services-types', methods=['GET'])
def obtener_tipos_de_servicios():
    """Obtiene los tipos de servicios

    Returns:
        dict: tipos de servicios
    """
    return Servicio.obtener_tipos()


def json_api(json):
    """Información de servicios
    Recorre el diccionario con la información de servicios y le actualiza
    los campos y retorna un diccionario con los campos necesarios"

    Args:
        json : diccionario con información de servicios

    Returns:
        data: diccionario con información de servicios
    """
    data = json["data"]
    for d in data:
        json_servicio(d)
    return data


def json_servicio(json):
    """información de un servicio

    Args:
        json: información del servicio

    Returns:
        json: diccionario con nuevos campos de servicio (quita el institucion_id y
        agrega el nombre de la institución a la que pertenece el servicio)
    """
    id_inst = json["institucion_id"]
    json.update({'institucion': str(Institucion.listar(id_inst).nombre)})
    json.pop('institucion_id')
    return json


@api_bp.post('/auth')
def autenticar():
    """Autentica a un usuario

    Returns:
        json: si las credenciales son válidas retorna un json con el id del
        usuario y un resultado exitoso. En caso contrario, retorna un json
        con un resultado fallido
    """
    if request.is_json:
        auth = request.get_json()
        usuario = Usuario.buscar_usuario_por_correo(auth["user"])
        if not usuario:
            return jsonify({'error': 'Parametros invalidos'}), 401
        if usuario.contraseña is None:
            return jsonify({'error': 'Parametros invalidos'}), 406
        if not usuario.obtener_estado():
            return jsonify({'error': 'Parametros invalidos'}), 403
        if not Usuario.chequear_contraseña(usuario.contraseña, auth["password"]):
            return jsonify({'error': 'Parametros invalidos'}), 401
        respuesta = jsonify({'token': Autenticacion.generar_token(usuario)})
        return respuesta, 201
    return jsonify({'error': 'UNSUPPORTED MEDIA TYPE'}), 415


@api_bp.post('/auth-google')
def autenticar_google():
    if request.is_json:
        auth = request.get_json()
        usuario = Usuario.buscar_usuario_por_correo(auth["correo"])
        if not usuario:
            return {"error": True, "mensaje": "Primero debe registrarse con Google"}, 401
        if not usuario.obtener_estado():
            return {"error": True, "mensaje": "Usted ha sido bloqueado. Hable con el administrador"}, 401
        token_acceso = Autenticacion.generar_token(usuario)
        if usuario.nombre_usuario is None:
            return {'token': token_acceso, "rellenar_formulario": True}, 201
        return {'token': token_acceso, "rellenar_formulario": False}, 201
    return {'error': 'UNSUPPORTED MEDIA TYPE'}, 415


@api_bp.post('/registro-correo')
def registrarse_correo():
    if request.is_json:
        usuario = request.get_json()
        genero = usuario["genero"]
        if genero == "O":
            genero_otro = usuario["genero_otro"]
        else:
            genero_otro = genero
        usr = {
            "correo": usuario["correo"],
            "contraseña": usuario["contraseña"],
            "nombre": usuario["nombre"],
            "nombre_usuario": usuario["nombre_usuario"],
            "apellido": usuario["apellido"],
            "tipo_documento": usuario["tipo_documento"],
            "nro_documento": usuario["nro_documento"],
            "genero": genero,
            "genero_otro": genero_otro,
            "telefono": usuario["telefono"],
            "direccion": usuario["direccion"],
            "es_super_admin": False,
            "activo": True,
            "es_cuenta_google": False
        }
        respuesta = {}
        respuesta_validacion = ValidarRegistroCorreoAPI.validate(usr)
        if not respuesta_validacion['is_valid']:
            respuesta = {"error": True, "mensajes": []}
            errores = respuesta_validacion["errores"]
            for error_info in errores.items():
                respuesta["mensajes"].append(error_info[1]["mensaje"])
            return respuesta, 400
        Usuario.crear_usuario(usr)
        respuesta = {"error": False, "mensajes": ["Usuario creado con exito"]}
        return respuesta, 201
    return jsonify({'error': 'UNSUPPORTED MEDIA TYPE'}), 415


@api_bp.post('/registro-google')
def datos_registro_google():
    if request.is_json:
        usuario = request.get_json()
        usr = {
            "correo": usuario["correo"],
            "nombre": usuario["nombre"],
            "apellido": usuario["apellido"]
        }
        respuesta = {}
        respuesta_validacion = ValidarRegistroGoogleAPI.validate(usr)
        if not respuesta_validacion['is_valid']:
            respuesta = {"error": True, "mensajes": []}
            errores = respuesta_validacion["errores"]
            for error_info in errores.items():
                respuesta["mensajes"].append(error_info[1]["mensaje"])
            return respuesta, 400
        Usuario.crear(correo=usuario["correo"], nombre=usuario["nombre"],
                      apellido=usuario["apellido"], es_super_admin=False,
                      activo=True, es_cuenta_google=True)
        respuesta = {"error": False, "mensajes": ["Usuario creado con exito"]}
        return respuesta, 201
    return {'error': True, 'mensajes': ['UNSUPPORTED MEDIA TYPE']}, 415


@api_bp.post('/completar-datos')
def completar_datos():
    if request.is_json:
        usuario = request.get_json()
        genero = usuario["genero"]
        if genero == "O":
            genero_otro = usuario["genero_otro"]
        else:
            genero_otro = genero
        usr = {
            "correo": usuario["correo"],
            "nombre_usuario": usuario["nombre_usuario"],
            "tipo_documento": usuario["tipo_documento"],
            "nro_documento": usuario["nro_documento"],
            "genero": genero,
            "genero_otro": genero_otro,
            "telefono": usuario["telefono"],
            "direccion": usuario["direccion"]
        }
        respuesta = {}
        respuesta_validacion = ValidarCompletarDatosGoogleAPI.validate(usr)
        if not respuesta_validacion['is_valid']:
            respuesta = {"error": True, "mensajes": []}
            errores = respuesta_validacion["errores"]
            for error_info in errores.items():
                respuesta["mensajes"].append(error_info[1]["mensaje"])
            return respuesta, 400
        Usuario.modificar_perfil_google(usr)
        respuesta = {"error": False, "mensajes": ["Datos completados con exito"]}
        return respuesta, 201
    return jsonify({'error': 'UNSUPPORTED MEDIA TYPE'}), 415


@api_bp.route('/me/profile', methods=['GET'])
@jwt_required()
def perfil_usuario():
    """Información del perfil del usuario logueado

    Returns:
        json: información del perfil del usuario logueado
    """
    usuario = Autenticacion.obtener_usuario_logueado()
    return Usuario.listar(usuario.id).json_perfil_api()


@api_bp.route('/me/requests', methods=['GET'])
@jwt_required()
@caracteres_validos
def obtener_solicitudes_de_servicios():
    """Obtener solicitudes de servicios

    Returns:
        json: información de solicitudes de servicio
    """   
    pagina = int(request.args.get('page', 1))
    por_pagina = int(request.args.get('per_page', Configuracion.get_elementos_por_pagina()))
    orden = request.args.get('order', "desc")
    ordenar_por = request.args.get('sort', "")
    atributos_excluidos_solicitudes = ["servicio_id", "usuario_id",
                                       "archivos_adjuntos", "nota_al_cliente"]
    usuario_id = Autenticacion.obtener_usuario_logueado().id
    return SolicitudServicio.listar_por_pagina_solicitudes_de_usuario(pagina, 
                                                                    por_pagina, usuario_id, 
                                                                    orden, ordenar_por,
                                                                    atributos_excluidos_solicitudes)


@api_bp.route('/me/requests/<int:id>', methods=['GET'])
@jwt_required()
def detalle_solicitud_de_servicio(id):
    """Obtiene el detalle de una solicitud de servicio 
        específica en formato json
    Args:
        id (int): id de la solicitud
    Returns:
        solicitud : información de la solicitud 
    """
    atributos_excluidos_solicitudes = ["servicio_id", "usuario_id",
                                     "archivos_adjuntos", "nota_al_cliente",
                                     "id"]
    if str(id).isdigit():
        solicitud = SolicitudServicio.listar(id)
        if solicitud is None:
            return abort(404)
        id_institucion = Servicio.listar(solicitud.servicio_id).institucion_id
        institucion = Institucion.listar(id_institucion)
        usuario_logueado = Autenticacion.obtener_usuario_logueado()
        if institucion.usuario_es_integrante(usuario_logueado) or solicitud.usuario_id == usuario_logueado.id or usuario_logueado.saber_si_es_super_usuario():
            solicitud = SolicitudServicio.obtener_solicitud_de_servicio(id, atributos_excluidos_solicitudes)
            if solicitud != {}:
                return solicitud
            else:
                return abort(404)
    return jsonify({"error": 'Parámetros inválidos'}), 400


@api_bp.route('/me/requests', methods=['POST'])
@jwt_required()
def nueva_solicitud_de_servicio():
    """nueva solicitud de servicio

    Returns:
        json: diccionario con información de la nueva solicitud
    """
    campos = ["titulo", "descripcion", "servicio"]
    if request.is_json:
        solicitud = request.get_json()
        if solicitud is not None and validar_campos_json(solicitud, campos):
            usuario_id = Autenticacion.obtener_usuario_logueado().id
            nueva_solicitud = SolicitudServicio.crear(titulo=solicitud["titulo"],
                                                      servicio_id=solicitud["servicio"],
                                                      usuario_id=usuario_id,
                                                      estado=EstadoEnum.CREADA,
                                                      detalle=solicitud["descripcion"])
            atributos_excluidos_solicitudes = ["servicio_id", "usuario_id", 
                                     "archivos_adjuntos", "nota_al_cliente",
                                     "actualizado_el"]
            return jsonify(SolicitudServicio.obtener_solicitud_de_servicio(
                nueva_solicitud.id, atributos_excluidos_solicitudes)), 201
    return jsonify({'error': 'parametros invalidos'}), 400


@api_bp.route('/me/requests/<int:id>/notes', methods=['POST'])
@jwt_required()
def cargar_nota_de_solicitud(id):
    """carga una nota a una solicitud especifica

    Args:
        id (int): id de la solicitud

    Returns:
        json: diccionario con información de la solitud
    """
    campos = ["nota"]
    id_usuario = Autenticacion.obtener_usuario_logueado().id
    if str(id).isdigit():
        if SolicitudServicio.listar(id) is None:
            return abort(404)
        if request.is_json:
            solicitud = request.get_json()
            if solicitud is not None and validar_campos_json(solicitud, campos):
                id_institucion = Servicio.listar(SolicitudServicio.listar(id).servicio_id).institucion_id
                institucion = Institucion.listar(id_institucion)
                usuario_logueado = Usuario.listar(id_usuario)
                if institucion.usuario_es_integrante(usuario_logueado) or (SolicitudServicio.listar(id).usuario_id == id_usuario) or usuario_logueado.saber_si_es_super_usuario():
                    nueva_nota = NotaSolicitud.crear(nota=solicitud["nota"],
                                                     solicitud_id=id,
                                                     usuario_id=id_usuario)
                    return jsonify({
                                    "id": nueva_nota.solicitud_id,
                                    "detalle": nueva_nota.nota
                                    }), 201
    return jsonify({'error': 'parametros invalidos'}), 400


def validar_campos_json(json, campos):
    """valida que se hayan ingresado todos los campos del json y
       que las claves también lo sean

    Args:
        json (dict): diccionario con datos ingresados
        campos (list): lista de campos requeridos

    Returns:
        bool: retorna True si las claves del json son correctos y
        false si alguna clave está mal escrita o no está
    """
    for c in campos:
        if c not in json:
            return False
    return True


@api_bp.route('/statistics/requests/by_state', methods=['GET'])
def solicitudes_realizadas_por_estado():
    """cantidad de solicitudes realizadas por estado

    Returns:
        dict: retorna un diccionario con la cantidad de solicitudes
        realizadas por estado
    """
    return jsonify(SolicitudServicio.cantidad_solicitudes_por_estado()), 200


@api_bp.route('/statistics/services/most_requested', methods=['GET'])
def servicios_mas_solicitados():
    """servicios mas solicitados

    Returns:
        dict: retorna un diccionario con los servicios 
        que tienen mas solicitudes
    """
    lista = []
    for serv in Servicio.listar_todos():
        lista.append({
            "servicio": serv.nombre,
            "solicitudes": len(Servicio.obtener_solicitudes(serv)), 
            "institucion": Institucion.listar(serv.obtener_institucion_id())
            .nombre
            })
    lista.sort(key=lambda servicio: servicio['solicitudes'], reverse=True)
    return jsonify({"data": lista}), 200


@api_bp.route('/statistics/institutions/best_resolution_time', methods=['GET'])
def intituciones_con_mejor_tiempo_de_resolución():
    """instituciones con mejor tiempo de resolución

    Returns:
        dict: retorna un diccionario con el tiempo de
        resolución promedio de instituciones. Si no
        hay instituciones que finalizaron solicitudes
        retorna un diccionario vacío
    """
    lista = []
    for inst in Institucion.listar_todos():
        tiempo = Institucion.tiempo_de_resolucion_promedio(inst)
        if tiempo is not None:
            lista.append({
                "institucion": inst.nombre,
                "tiempo_promedio": round(tiempo, 1), 
                })
    lista.sort(key=lambda institucion: institucion['tiempo_promedio'])
    return jsonify({"data": lista[:10]}), 200


@api_bp.route('/services/searcher', methods=['GET'])
@caracteres_validos
def buscador_de_servicios():
    """Obtener servicios buscados

    Returns:
        json: diccionario de servicios buscados
    """
    pagina = int(request.args.get('page', 1))
    por_pagina = int(request.args.get('per_page', Configuracion.get_elementos_por_pagina()))
    tipo = request.args.get('type', "")
    descripcion_servicio = request.args.get('service_description', "")
    nombre_servicio = request.args.get('service_name', "")
    tag = request.args.get('tag', "")
    nombre_institucion = request.args.get('institution_name', "")
    atributos_excluidos_servicios = ["creado_el", "actualizado_el"]
    return Servicio.buscar_servicios(tipo, tag, descripcion_servicio, nombre_servicio, pagina, por_pagina, 
                                     nombre_institucion, atributos_excluidos_servicios)


@api_bp.route('/services/all_services', methods=['GET'])
@caracteres_validos
def listar_todos_los_servicios():
    """Obtener todos los servicios

    Returns:
        json: diccionario con todos los servicios
    """   
    pagina = int(request.args.get('page', 1))
    por_pagina = int(request.args.get('per_page', Configuracion.get_elementos_por_pagina()))
    atributos_excluidos_servicios = ["creado_el", "actualizado_el"]
    return Servicio.obtener_servicios(pagina, por_pagina, atributos_excluidos_servicios)


@api_bp.route('/institutions/<string:nombre>', methods=['GET'])
def obtener_institucion(nombre):
    """Obtiene una institución especifica en formato json
    Args:
        nombre (str): nombre de la institución
    Returns:
        institución : información de la institución 
    """
    institucion = Institucion.obtener_institucion_por_nombre(nombre)
    if institucion is None:
        return abort(404)
    return institucion.json(atributos_excluidos_instituciones), 200

@api_bp.route('/requests/<int:id>/get_notes', methods=['GET'])
@caracteres_validos
def obtener_notas_de_solicitud(id):
    """Obtiene las notas de una solicitud especifica 
        en formato json

    Args:
        id (int): nombre de la solicitud

    Returns:
        json_notas : información de las notas de una solicitud 
    """
    pagina = int(request.args.get('page', 1))
    por_pagina = int(request.args.get('per_page', 0))
    if str(id).isdigit():
        solicitud = SolicitudServicio.listar(id)
        if solicitud is not None:
            return NotaSolicitud.obtener_notas_con_remitente(id, pagina, por_pagina)
        return abort(404)


@api_bp.route('/institutions/geocoding/<string:direccion>', methods=['GET'])
def obtener_coordenadas(direccion):
    """Obtiene las coordenadas (latitud y longitud) en funcion de la direccion 
    de la institucion, en formato json
    Args:
        direccion (str): direccion de la institución
    Returns:
        coordenadas : coordenadas de la direccion de la institución
    """

    geolocator = Nominatim(user_agent="my_geocoder")
    # Convierto las coordenadas de la dirección
    coordenadas = geolocator.geocode(direccion)
    coordenadas_dict = {"latitude": coordenadas.latitude, "longitude": coordenadas.longitude}
    coordenadas_json = json.dumps(coordenadas_dict)
    if coordenadas is None:
        return abort(404)
    return coordenadas_json, 200


@api_bp.get('/info-contacto')
def obtener_info_contacto():
    info = Configuracion.get_info_contacto()
    if info == '':
        return {'info_contacto': "No hay información de contacto"}
    return {'info_contacto': Configuracion.get_info_contacto()}

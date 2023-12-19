from src.core.models.usuario import Usuario
from src.core.models.token import Token
import re


class ErrorValidacion(Exception):
    def __init__(self, msg="", estado="", *args: object) -> None:
        super().__init__(msg, *args)
        self.estado = estado


def validar_sea_string(value: str) -> str:
    if not isinstance(value, str):
        raise ErrorValidacion(f"El campo no es string, el tipo es {str(type(value))}", "warning")
    return value


def validar_sea_boolean(value: str) -> str:
    if not isinstance(value, bool):
        raise ErrorValidacion(f"El campo no es booleano, el tipo es {str(type(value))}", "warning")
    return value


def validar_sea_integer(value: str) -> str:
    if not isinstance(value, int):
        raise ErrorValidacion(f"El campo no es entero, el tipo es {str(type(value))}", "warning")
    return value


def validar_no_haya_espacios(value: str) -> str:
    if any(i.isspace() for i in value):
        raise ErrorValidacion(f"El campo contiene espacios, el valor es {str(type(value))}", "warning")
    return value


def campo_vacio(campo: str) -> str:
    """ Verifica si los parametros no estan vacios"""
    if not len(campo):
        raise ErrorValidacion("Todos los campos son obligatorios", "danger")
    return campo


def validacion_correo(correo: str) -> str:
    """ Verifica si el string ingresado tiene formato de correo """
    if re.match(
        "^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$",
        correo.lower(),
    ):
        return correo
    else:
        raise ErrorValidacion("Formato invalido de correo", "danger")


def correo_en_uso(correo: str) -> str:
    """ Verifica si el correo pasado por parametro ya esta en la BD """
    usuario = Usuario.buscar_usuario_por_correo(correo)
    if usuario is not None:
        raise ErrorValidacion("Este correo ya esta en uso", "danger")
    else:
        return correo


def nombre_usuario_en_uso(nombre_usuario: str) -> str:
    """ Verifica si el nombre de usuario pasado por parametro ya esta en la BD"""
    usuario = Usuario.buscar_usuario_por_nombre_usuario(nombre_usuario)
    if usuario is not None:
        raise ErrorValidacion("Este nombre de usuario ya esta en uso", "danger")
    else:
        return nombre_usuario


def validacion_tipo_documento(tipo_docu: str) -> str:
    tipos_validos = ("dni", "civica", "enrolamiento")
    for tipo in tipos_validos:
        if tipo_docu == tipo:
            return tipo_docu
    raise ErrorValidacion("Tipo invalido de documento", "danger")


def validacion_genero(genero: str) -> str:
    tipos_validos = ("M", "F", "O", "P")
    for tipo in tipos_validos:
        if genero == tipo:
            return genero
    raise ErrorValidacion("Valor invalido para el genero", "danger")


def completo_preregistro(token: str) -> bool:
    """ Verifica si el usuario debe completar el registro final """
    usuario = Token.buscar_usuario_con_token(token)
    if usuario is None:
        raise ErrorValidacion('Token inexistente en el sistema. Asegurese de haber completado el preregistro o haber escrito correctamente el token', "danger")
    elif usuario.contraseña is not None:
        raise ErrorValidacion('Usted ya completo el proceso para registrarse, solamente debe iniciar sesion', "warning")
    return token


class ValidarSerializador():
    fields = {}

    @classmethod
    def validate(cls, data: dict):
        errores = {}
        for campo, funciones_validacion in cls.fields.items():
            try:
                for funcion_validar in funciones_validacion:
                    data[campo] = funcion_validar(data[campo])
            except ErrorValidacion as e:
                errores[campo] = {"mensaje": str(e), "estado": e.estado}
            except KeyError:
                pass
        return {"is_valid": not errores, "errores": errores}


class ValidarPreRegistro(ValidarSerializador):
    fields = {
        "nombre": [campo_vacio, validar_sea_string],
        "apellido": [campo_vacio, validar_sea_string],
        "correo": [campo_vacio, validacion_correo, correo_en_uso],
        "tipo_documento": [campo_vacio, validacion_tipo_documento],
        "nro_documento": [campo_vacio, validar_sea_string],
        "direccion": [campo_vacio, validar_sea_string],
        "genero": [campo_vacio, validar_sea_string, validacion_genero],
        "genero_otro": [campo_vacio, validar_sea_string],
        "telefono": [campo_vacio, validar_sea_string]
    }


class ValidarRegistro(ValidarSerializador):
    fields = {
        "nombre_usuario": [campo_vacio, validar_sea_string,
                           nombre_usuario_en_uso],
        "contraseña": [campo_vacio, validar_sea_string],
        "token": [campo_vacio, completo_preregistro],
    }


class ValidarCrearUsuario(ValidarSerializador):
    fields = {
        "nombre": [campo_vacio, validar_sea_string],
        "apellido": [campo_vacio, validar_sea_string],
        "correo": [campo_vacio, validacion_correo, correo_en_uso],
        "tipo_documento": [campo_vacio, validacion_tipo_documento],
        "nro_documento": [campo_vacio, validar_sea_string],
        "direccion": [campo_vacio, validar_sea_string],
        "genero": [campo_vacio, validar_sea_string, validacion_genero],
        "genero_otro": [campo_vacio, validar_sea_string],
        "telefono": [campo_vacio, validar_sea_string],
        "nombre_usuario": [campo_vacio, validar_sea_string,
                           nombre_usuario_en_uso],
        "contraseña": [campo_vacio, validar_sea_string],
    }


class ValidarModificarPerfil(ValidarSerializador):
    fields = {
        "nombre": [campo_vacio, validar_sea_string],
        "apellido": [campo_vacio, validar_sea_string],
        "tipo_documento": [campo_vacio, validacion_tipo_documento],
        "nro_documento": [campo_vacio, validar_sea_string],
        "direccion": [campo_vacio, validar_sea_string],
        "genero": [campo_vacio, validar_sea_string, validacion_genero],
        "genero_otro": [campo_vacio, validar_sea_string],
        "telefono": [campo_vacio, validar_sea_string],
        "nombre_usuario": [campo_vacio, validar_sea_string],
        "contraseña": [campo_vacio],
    }


class ValidarModificarUsuario(ValidarSerializador):
    fields = {
        "nombre": [campo_vacio, validar_sea_string],
        "apellido": [campo_vacio, validar_sea_string],
        "tipo_documento": [campo_vacio, validacion_tipo_documento],
        "nro_documento": [campo_vacio, validar_sea_string],
        "direccion": [campo_vacio, validar_sea_string],
        "genero": [campo_vacio, validar_sea_string, validacion_genero],
        "genero_otro": [campo_vacio, validar_sea_string],
        "telefono": [campo_vacio, validar_sea_string],
        "nombre_usuario": [campo_vacio, validar_sea_string],
        "contraseña": [campo_vacio],
        "activo": [validar_sea_boolean]
    }


class ValidarRegistroCorreoAPI(ValidarSerializador):
    fields = {
        "nombre": [campo_vacio, validar_sea_string],
        "apellido": [campo_vacio, validar_sea_string],
        "correo": [campo_vacio, validacion_correo, correo_en_uso],
        "nombre_usuario": [campo_vacio, validar_sea_string,
                           nombre_usuario_en_uso],
        "contraseña": [campo_vacio, validar_sea_string],
        "tipo_documento": [campo_vacio, validacion_tipo_documento],
        "nro_documento": [campo_vacio, validar_sea_string],
        "direccion": [campo_vacio, validar_sea_string],
        "genero": [campo_vacio, validar_sea_string, validacion_genero],
        "genero_otro": [campo_vacio, validar_sea_string],
        "telefono": [campo_vacio, validar_sea_string]
    }


class ValidarRegistroGoogle(ValidarSerializador):
    fields = {
        "correo": [campo_vacio, validacion_correo, correo_en_uso],
        "tipo_documento": [campo_vacio, validacion_tipo_documento],
        "nro_documento": [campo_vacio, validar_sea_string],
        "direccion": [campo_vacio, validar_sea_string],
        "genero": [campo_vacio, validar_sea_string, validacion_genero],
        "genero_otro": [campo_vacio, validar_sea_string],
        "telefono": [campo_vacio, validar_sea_string],
        "nombre_usuario": [campo_vacio, nombre_usuario_en_uso]
    }


class ValidarModificarPerfilGoogle(ValidarSerializador):
    fields = {
        "nombre": [campo_vacio, validar_sea_string],
        "apellido": [campo_vacio, validar_sea_string],
        "tipo_documento": [campo_vacio, validacion_tipo_documento],
        "nro_documento": [campo_vacio, validar_sea_string],
        "direccion": [campo_vacio, validar_sea_string],
        "genero": [campo_vacio, validar_sea_string, validacion_genero],
        "genero_otro": [campo_vacio, validar_sea_string],
        "telefono": [campo_vacio, validar_sea_string],
        "nombre_usuario": [campo_vacio, validar_sea_string],
        "contraseña": [campo_vacio],
    }


class ValidarRegistroGoogleAPI(ValidarSerializador):
    fields = {
        "correo": [campo_vacio, validacion_correo, correo_en_uso],
        "nombre": [campo_vacio, validar_sea_string],
        "apellido": [campo_vacio, validar_sea_string],
    }


class ValidarCompletarDatosGoogleAPI(ValidarSerializador):
    fields = {
        "tipo_documento": [campo_vacio, validacion_tipo_documento],
        "nro_documento": [campo_vacio, validar_sea_string],
        "direccion": [campo_vacio, validar_sea_string],
        "genero": [campo_vacio, validar_sea_string, validacion_genero],
        "genero_otro": [campo_vacio, validar_sea_string],
        "telefono": [campo_vacio, validar_sea_string],
        "nombre_usuario": [campo_vacio, validar_sea_string,
                           nombre_usuario_en_uso],
    }

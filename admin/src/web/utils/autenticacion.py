from src.core.models.usuario import Usuario
from flask_jwt_extended import create_access_token, get_jwt_identity


class Autenticacion():

    @classmethod
    def generar_token(cls, usuario):
        return create_access_token(identity=usuario.id)

    @classmethod
    def obtener_usuario_logueado(cls):
        usuario = get_jwt_identity()
        return Usuario.listar(usuario)

from src.core.basededatos import db
from src.core.models.usuario import Usuario
import secrets


class Token(db.Model):
    __tablename__ = "token"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    token = db.Column(db.String(255), nullable=False, unique=True)
    correo_usuario = db.Column(db.String(255), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def generar_token(cls, usr: dict) -> str:
        """Genera un token de 10 caracteres
           (valida si ese token ya existe)

        Returns:
            str: el token generado
        """
        correo = usr["correo"]
        buscar_token_unico = True
        while buscar_token_unico:
            string_token = secrets.token_urlsafe(15)
            encontre_token = Token.query.filter_by(token=string_token).first()
            if encontre_token is None:
                buscar_token_unico = False
        token = Token(token=string_token, correo_usuario=correo)
        db.session.add(token)
        db.session.commit()
        return string_token

    @classmethod
    def buscar_usuario_con_token(cls, token: str) -> object:
        """Busca al usuario que tenga ese token, si no existe
           retorna nulo

        Args:
            token (str): token que se va a buscar

        Returns:
            object: usuario que tenga ese token (o None si no existe)
        """
        token = Token.query.filter_by(token=token).first()
        if token is None:
            return None
        usuario = Usuario.query.filter_by(correo=token.correo_usuario).first()
        return usuario

    @classmethod
    def eliminar_token(cls, string_token: str):
        token = Token.query.filter_by(token=string_token).first()
        db.session.delete(token)
        db.session.commit()

    @classmethod
    def eliminar_token_con_correo(cls, correo: str):
        token = Token.query.filter_by(correo_usuario=correo).first()
        if token is not None:
            db.session.delete(token)
            db.session.commit()

from datetime import datetime
from src.core.basededatos import db
from src.core.models.permiso import Permiso
from src.core.models.base import BaseModel


rol_tiene_permisos = db.Table(
    'rol_tiene_permisos',
    db.Column('rol_id', db.ForeignKey('roles.id')),
    db.Column('permiso_id', db.ForeignKey(Permiso.id)))


class Rol(BaseModel):
    __tablename__ = "roles"
    nombre = db.Column(db.String(255), nullable=False)
    permisos = db.relationship('Permiso', secondary=rol_tiene_permisos)

    def obtener_permisos(self):
        """Retorna los permisos que tiene ese rol"""
        return self.permisos

    @classmethod
    def obtener_rol(cls, nombre: str) -> int:
        """obtener_rol

        Args:
            nombre (str): nombre del rol

        Returns:
            rol: retorna el rol segun el nombre por parametro
        """
        rol = Rol.query.filter_by(nombre=nombre).first()
        return rol

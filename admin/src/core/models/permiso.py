from datetime import datetime
from src.core.basededatos import db
from src.core.models.base import BaseModel


class Permiso(BaseModel):
    __tablename__ = "permisos"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(255), nullable=False)
    creado_el = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_el = db.Column(db.DateTime, default=datetime.utcnow,
                               onupdate=datetime.utcnow)

    @classmethod
    def crear(cls, nombre: str) -> object:
        """_summary_

        Args:
            nombre (str): nombre del permiso

        Returns:
            permiso: retorna el permiso creado
        """
        permiso = Permiso(nombre=nombre)
        db.session.add(permiso)
        db.session.commit()
        return permiso

    @classmethod
    def listar_por_nombre(cls, nombre: str) -> object:
        """Obtener un objeto por su nombre."""
        return cls.query.filter_by(nombre=nombre).first()

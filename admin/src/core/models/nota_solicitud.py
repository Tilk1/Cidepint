from src.core.models.usuario import Usuario
from src.core.basededatos import db
from src.core.models.base import BaseModel


class NotaSolicitud(BaseModel):
    __tablename__ = "notas"
    nota = db.Column(db.String(255), nullable=False)
    solicitud_id = db.Column(db.Integer, db.ForeignKey("solicitudes.id", ondelete='CASCADE'),
                             nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete='CASCADE'),
                           nullable=False)
    
    @classmethod
    def obtener_notas_con_remitente(cls, id_solicitud,  pagina, por_pagina):

        """Obtiene el detalle de las notas y sus remitentes

        Args:
            id_solicitud (int): id de la solicitud
            pagina (int): página actual
            por_pagina (int): elementos por página

        Returns:
            json: diccionario con notas y sus remitentes
            de una solicitud de servicio
        """

        lista = []
        notas = db.session.query(NotaSolicitud, Usuario).join(Usuario).filter(
            NotaSolicitud.usuario_id == Usuario.id,
            NotaSolicitud.solicitud_id == id_solicitud)
         
        total = notas.count()

        if por_pagina == 0:
            inicio = (pagina - 1) * total
            fin = inicio + total
        else:
            inicio = (pagina - 1) * por_pagina
            fin = inicio + por_pagina

        notas = notas.slice(inicio, fin)
        for nota_solicitud, usuario in notas.all():
            json = {}
            json_nota = {}
            for column in nota_solicitud.__table__.columns:
                if "usuario" not in column.name:
                    json_nota[column.name] = getattr(nota_solicitud, column.name)
            json_usuario = {}
            for column in usuario.__table__.columns:
                if "contraseña" not in column.name:
                    json_usuario[column.name] = getattr(usuario, column.name)
            json["nota"] = json_nota
            json["usuario"] = json_usuario
            lista.append(json)
            lista.sort(key=lambda nota: nota["nota"]['creado_el'])
        arch = {
            "data": lista,
            "total": total,
            "page": pagina,
            "per_page": por_pagina,
        }
        return arch
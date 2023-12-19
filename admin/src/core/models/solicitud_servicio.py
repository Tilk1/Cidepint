from src.core.basededatos import db
from src.core.models.base import BaseModel
from enum import Enum
from datetime import datetime
from functools import reduce
from src.core.models.servicio import Servicio
from src.core.models.usuario import Usuario


class EstadoEnum(Enum):
    CREADA = "Creada"
    ACEPTADA = "Aceptada"
    RECHAZADA = "Rechazada"
    EN_PROCESO = "En proceso"
    FINALIZADA = "Finalizada"
    CANCELADA = "Cancelada"


class SolicitudServicio(BaseModel):
    __tablename__ = "solicitudes"
    titulo = db.Column(db.String(255), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey("servicios.id", ondelete='CASCADE'),
                            nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete='CASCADE'),
                           nullable=False)
    detalle = db.Column(db.String(255), nullable=False)
    archivos_adjuntos = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.Enum(EstadoEnum), nullable=False)
    cerrada_el = db.Column(db.DateTime, nullable=True)
    notas = db.relationship('NotaSolicitud', backref='solicitudes', lazy=True, cascade="all, delete-orphan")

    # to do refactorizar
    @classmethod
    def listar_filtrado(cls, solicitante: str, tipo: str, estado: str,
                        desde: str, hasta: str, institucion_id: int):
        """Filtra las solicitudes por los parametros indicados

        Args:
            pagina (int): pagina
            elementos_por_pagina (int): elementos por pagina
            solicitante (str):  nombre del solicitante
            tipo (str): todos/analisis/consultoria/desarrollo
            estado (str): todos/aceptada/rechazada/en proceso/finalizada/..
            desde (str): fecha desde la cual se quiere filtrar
            hasta (str): fecha hasta la cual se quiere filtrar
        """
        consultas = []
        if institucion_id and institucion_id != "None":
            consultas.append(set(cls.listar_filtrado_por_institucion(institucion_id)))
        if solicitante != "":
            consultas.append(set(cls.listar_filtrado_por_solicitante(solicitante)))
        if tipo != "Todos":
            consultas.append(set(cls.listar_filtrado_por_tipo(tipo)))
        if estado != "Todos":
            consultas.append(set(cls.listar_filtrado_por_estado(estado)))
        if desde and desde != "":
            desde = datetime.strptime(desde, "%d/%m/%Y")
            consultas.append(set(cls.listar_filtrado_por_desde(desde)))
        if hasta and hasta != "":
            hasta = datetime.strptime(hasta, "%d/%m/%Y")
            consultas.append(set(cls.listar_filtrado_por_hasta(hasta)))

        if consultas:
            resultado_interseccion = reduce(lambda x, y: x.intersection(y), consultas)
            resultado_lista = list(resultado_interseccion)
            return resultado_lista
        else:
            return cls.listar_todos()

    @classmethod
    def listar_filtrado_por_institucion(cls, institucion_id: int):
        """Filtra por institucion

        Args:
            institucion_id (int): id de la institucion,
            obtiene las solicitudes unicamente de una institucion
            pasando por todos sus servicios

        Returns:
            objects: solicitudes filtradas
        """
        return db.session.query(cls).join(Servicio).filter(Servicio.institucion_id == institucion_id).all()

    @classmethod
    def listar_filtrado_por_tipo(cls, tipo: str):
        """Filtra por tipo de servicio

        Args:
            tipo (str): tipo de servicio,
            se obtiene por medio servicio_id
            hace un join con la tabla servicio

        Returns:
            objects: solicitudes filtradas
        """
        return db.session.query(cls).join(Servicio).filter(Servicio.tipo == tipo).all()

    @classmethod
    def listar_filtrado_por_estado(cls, estado: str):
        """Filtra por estado de la solicitud

        Args:
            estado (str): estado de la solicitud

        Returns:
            objects: solicitudes filtradas
        """
        estado_enum = EstadoEnum(estado)
        return db.session.query(cls).filter(cls.estado == estado_enum).all()

    @classmethod
    def listar_filtrado_por_solicitante(cls, solicitante: str):
        """Filtra por solicitante

        Args:
            solicitante (str): solicitante de la solicitud,
            se obtiene por medio usuario_id
            hace un join con la tabla usuario

        Returns:
            objects: solicitudes filtradas
        """
        return db.session.query(cls).join(Usuario).filter((Usuario.nombre.like(f"%{solicitante}%"))).all()

    @classmethod
    def listar_filtrado_por_desde(cls, desde: str):
        """Filtra por fechas de creacion mayores a la fecha indicada

        Args:
            desde (str): fecha desde la cual se quiere filtrar

        Returns:
            objects: solicitudes filtradas
        """
        return cls.query.filter(cls.creado_el >= desde).all()


    @classmethod
    def listar_filtrado_por_hasta(cls, hasta: str):
        """Filtra por fechas de creacion menores a la fecha indicada

        Args:
            hasta (str): fecha hasta la cual se quiere filtrar

        Returns:
            objects: solicitudes filtradas
        """
        return cls.query.filter(cls.creado_el <= hasta).all()

    def json_solicitud(self, atributos_excluidos=None):
        """información de una solicitud de servicio

        Args: 
            atributos_excluidos (list): lista de atributos excluidos en el json

        Returns:
            json: diccionario con información de una solicitud de servicio
        """
        if atributos_excluidos is None:
            atributos_excluidos = []

        informacion = {}
        for column in self.__table__.columns:
            if column.name not in atributos_excluidos:
                if column.name == "estado":
                    informacion[column.name] = self.estado.value
                else:
                    informacion[column.name] = getattr(self, column.name)

        return informacion

    @classmethod
    def listar_por_pagina_solicitudes_de_usuario(cls, pagina, por_pagina, 
                                               id_usuario, orden, ordenar_por,
                                               atributos_excluidos=None):
        """lista por página solicitudes de servicios

        Args:
            pagina (int): página actual
            por_pagina (int): cantidad por página
            id_usuario (int): id del usuario logueado
            orden(str): orden descendente o ascendente 
            ordenar_por(str): criterio de ordenación
            atributos_excluidos (list): lista de atributos excluidos en el json

        Returns:
            arch : retorna un json con las solicitudes de servicios
        """
        inicio = (pagina - 1) * por_pagina
        fin = inicio + por_pagina
        lista = []
        solicitudes = SolicitudServicio.query.filter(SolicitudServicio.
                                                     usuario_id == id_usuario)
        total = solicitudes.count()
        for solicitud in solicitudes:
            lista.append(solicitud.json_solicitud(atributos_excluidos))

        lista_claves = ["titulo", "creado_el", "actualizado_el", "estado"] 

        if ordenar_por == "" or ordenar_por not in lista_claves:
            ordenar_por = "id"

        if orden == "asc":
            lista = sorted(lista, key=lambda x: x[ordenar_por], reverse=False)
        else: 
            lista = sorted(lista, key=lambda x: x[ordenar_por], reverse=True)

        arch = {
            "data": lista[inicio:fin],
            "page": pagina,
            "per_page": por_pagina,
            "total": total
        }
        return arch

    @classmethod
    def obtener_solicitud_de_servicio(cls, id, atributos_excluidos=None):
        """Obtiene el detalle de un servicio específico
           en un diccionario

        Args:
            id (int): id del servicio
            atributos_excluidos (list): lista de atributos excluidos en el json

        Returns:
            servicio: el detalle de un servicio
        """
        solicitud = SolicitudServicio.query.filter_by(id=id).first()
        if solicitud:
            return solicitud.json_solicitud(atributos_excluidos)
        return {}

    def actualizar_valor(self, campo: str, valor):
        """Actualiza un campo de la tabla en la base de datos 

        Args:
            campo (str): campo a modificar en la tabla solicitud de servicio
            valor: valor que contendrá el campo
        """
        setattr(self, campo, valor)
        db.session.commit()

    def obtener_notas(self):
        """Obtiene las notas de una solicitud de servicio

        Returns:
            notas: las notas de una solicitud de servicio
        """
        return self.notas
    
    def obtener_servicio(self) -> object:
        """Obtiene el servicio que corresponde a la solicitud

        Returns:
            object: el servicio
        """
        return Servicio.listar(self.servicio_id)
    
    @classmethod
    def cantidad_solicitudes_por_estado(cls):
        """ cantidad de solicitudes realizadas por 
            estado
        
        Returns:
            dict: retorna un diccionario con la cantidad de solicitudes 
            realizadas por estado
        """
        diccionario_estados = {}
        for i in EstadoEnum:
            diccionario_estados[i.value] = len(SolicitudServicio.listar_filtrado_por_estado(i.value))
        return diccionario_estados
    
    def tiempo_de_resolucion_solicitud(self):
        """tiempo de resolución de una solicitud 

        Returns:
            datetime: retorna un datetime si la solicitud está finalizada,
            sino retorna None
        """
        if self.cerrada_el is not None:
            return self.cerrada_el - self.creado_el
        return None
    
    def actualizar_cierre_solicitud(self):
        """
           Actualiza la fecha de cierre de una
           solicitud
        """
        if self.estado.value == "Finalizada":
            self.cerrada_el = datetime.utcnow()
        else:
            self.cerrada_el = None
        db.session.commit()
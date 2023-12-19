import enum
from src.core.basededatos import db
from src.core.models.institucion import Institucion
from src.core.models.base import BaseModel  
from sqlalchemy import and_


class Tipos(enum.Enum):
    analisis = "Análisis"
    consultoria = "Consultoría"
    desarrollo = "Desarrollo"


class Servicio(BaseModel):
    __tablename__ = "servicios"
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    palabras_claves = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(255), nullable=False)
    habilitado = db.Column(db.Boolean)
    institucion_id = db.Column(db.Integer, db.ForeignKey(Institucion.id),
                               nullable=True)

    @classmethod
    def listar_por_pagina_y_tipo(cls, tipo_serv, q, pagina, por_pagina,
                                 atributos_excluidos=None):
        """lista servicios por página, término de búsqueda y tipo
           en formato json
        Args:
            pagina (int): número de página
            por_pagina (int): cantidad de elementos por página
            tipo_serv (str): tipo de servicio
            q (str): término de búsqueda
        Returns:
            arch: lista de servicios
        """
        inicio = (pagina - 1) * por_pagina
        fin = inicio + por_pagina
        if (tipo_serv is not None):
            servicios = Servicio.query.filter(Servicio.palabras_claves.like(
                f"%{q}%"), Servicio.tipo == tipo_serv)
        else:
            servicios = Servicio.query.filter(Servicio.palabras_claves.like(
                f"%{q}%"))
        total = servicios.count()
        servicios = servicios.slice(inicio, fin)
        lista = []
        for servicio in servicios:
            lista.append(servicio.json(atributos_excluidos))
        arch = {
            "data": lista,
            "page": pagina,
            "per_page": por_pagina,
            "total": total
        }
        return arch

    @classmethod
    def obtener_detalle_de_servicio(cls, id, atributos_excluidos=None):
        """Obtiene el detalle de un servicio específico
           en un diccionario
        Args:
            id (int): id del servicio
        Returns:
            servicio: el detalle de un servicio
        """
        servicio = Servicio.query.filter_by(id=id).first()
        if servicio:
            return servicio.json(atributos_excluidos)
        return {}

    @classmethod
    def obtener_tipos(cls):
        """obtiene los tipos de servicios

        Returns:
            dict: tipos de servicios
        """
        tipos = []
        for i in Tipos:
            tipos.append(i.value)
        return {'data': tipos}

    def obtener_solicitudes(self) -> list:
        from src.core.models.solicitud_servicio import SolicitudServicio
        """obtener_solicitudes

        Returns:
            list: retorna una lista de solicitudes
        """
        solicitudes = db.session.query(SolicitudServicio).filter(
            SolicitudServicio.servicio_id == self.id).all()
        return solicitudes

    @classmethod
    def paginar_servicios_institucion(cls, id, pagina, por_pagina,
                                      atributos_excluidos=None):
        inicio = (pagina - 1) * por_pagina
        fin = inicio + por_pagina
        lista = []
        institucion = Institucion.listar(id)
        lista_serv = institucion.obtener_servicios()
        servicios = lista_serv[inicio:fin]
        for servicio in servicios:
            lista.append(servicio.json(atributos_excluidos))
        arch = {
            "data": lista,
            "page": pagina,
            "per_page": por_pagina,
            "total": len(lista_serv)
        }
        return arch

    def obtener_institucion_id(self):
        return self.institucion_id
    
    def obtener_tiempo_promedio_resolucion(self):
        """tiempo promedio de resolución de solicitudes 
            de un servicio

        Returns:
            float: retorna un float si hay solicitudes finalizadas,
            sino retorna None
        """
        lista = []
        for solicitud in self.obtener_solicitudes():
            tiempo = solicitud.tiempo_de_resolucion_solicitud()
            if tiempo is not None:
                lista.append(tiempo.days)
        if lista:
            return sum(lista) / len(lista)
        return None

    @classmethod
    def buscar_servicios(cls, tipo_serv, tag, descrip, nombre_serv, pagina, 
                         por_pagina, nombre_inst, atributos_excluidos=None):
        """lista servicios por página, término de búsqueda y tipo
           en formato json
        Args:
            pagina (int): número de página
            por_pagina (int): cantidad de elementos por página
            tipo_serv (str): tipo de servicio
            tag(str): palabra clave 
            descrip(str): descripción del servicio buscado
            nombre_serv(str): nombre del servicio buscado
            nombre_inst(str): nombre de la institución buscada
            atributos_excluidos(list): atributos que no deben incluirse en
            el json
        Returns:
            arch: lista de servicios
        """
        inicio = (pagina - 1) * por_pagina
        fin = inicio + por_pagina
        lista_filtros = []
        servicios = Servicio.query
        if tipo_serv != "":
            lista_filtros.append(Servicio.tipo == tipo_serv)
        if tag != "":
            lista_filtros.append(db.func.lower(Servicio.palabras_claves)
                                 .like(f"%{tag.lower()}%"))
        if descrip != "":
            lista_filtros.append(db.func.lower(Servicio.descripcion)
                                 .like(f"%{descrip.lower()}%"))
        if nombre_serv != "":
            lista_filtros.append(db.func.lower(Servicio.nombre)
                                 .like(f"%{nombre_serv.lower()}%"))
        if nombre_inst != "":
            lista_filtros.append(Servicio.institucion_id.in_
                                 (Institucion.filtrar_nombres(nombre_inst)))

        if lista_filtros:
            servicios = servicios.filter(and_(*lista_filtros))

        total = servicios.count()
        servicios = servicios.slice(inicio, fin)
        lista = []
        for servicio in servicios:
            servicio = servicio.json(atributos_excluidos)
            servicio["institucion"] = Institucion.listar(servicio[
                "institucion_id"]).nombre
            servicio.pop("institucion_id")
            lista.append(servicio)
        arch = {
            "data": lista,
            "page": pagina,
            "per_page": por_pagina,
            "total": total
        }
        return arch
    
    @classmethod
    def obtener_servicios(cls, pagina, por_pagina,
                                 atributos_excluidos=None):
        """lista servicios por página, término de búsqueda y tipo
           en formato json

        Args:
            pagina (int): número de página
            por_pagina (int): cantidad de elementos por página
            atributos_excluidos(list): lista de atributos a excluir en el json

        Returns:
            arch: lista de servicios
        """
        inicio = (pagina - 1) * por_pagina
        fin = inicio + por_pagina

        servicios = Servicio.query
        total = servicios.count()
        servicios = servicios.slice(inicio, fin)
        lista = []
        for servicio in servicios:
            servicio = servicio.json(atributos_excluidos)
            servicio["institucion"] = Institucion.listar(servicio[
                "institucion_id"]).nombre
            servicio.pop("institucion_id")
            lista.append(servicio)
        arch = {
            "data": lista,
            "page": pagina,
            "per_page": por_pagina,
            "total": total
        }
        return arch

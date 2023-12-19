from datetime import datetime
from src.core.basededatos import db


class BaseModel(db.Model):
    """Clase abstracta que proporciona operaciones CRUD para los modelos"""

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, unique=True)
    creado_el = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_el = db.Column(db.DateTime, default=datetime.utcnow,
                               onupdate=datetime.utcnow)

    @classmethod
    def crear(cls, **kwargs) -> object:
        """Crea un nuevo objeto y guardarlo en la base de datos

        Params:
            kwargs: atributos del objeto a crear

        Returns:
            object: objeto creado
        """
        instance = cls(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def listar(cls, id: int) -> object:
        """Busca un objeto por su id

        Params:
            id: id del objeto a buscar
        Returns:
            object: objeto encontrado
        """
        return db.session.get(cls, id)

    @classmethod
    def listar_todos(cls) -> list:
        """Obtiene todas las filas del modelo

        Returns:
            list: lista de objetos
        """
        return db.session.query(cls).all()

    @classmethod
    def contar_todos(cls) -> int:
        """Cuenta todos los objetos del modelo

        Returns:
            int: numero de objetos
        """
        return db.session.query(cls).count()

    def eliminar(self) -> None:
        """Eliminar el objeto de la base de datos

        Returns:
            None
        """
        db.session.delete(self)
        db.session.commit()

    def modificar(self, **kwargs) -> None:
        """Modificar el objeto con nuevos valores y guardarlo en la db

        Params:
            kwargs: atributos del objeto a modificar

        Returns:
            None
        """
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        db.session.commit()

    def json(self, atributos_excluidos=None) -> dict:
        """Retorna un diccionario con los atributos del objeto
        quitando los atributos especificados en el parametro
        lista de atributos excluidos

        Params:
            list: atributos excluidos del diccionario

        Returns:
            dict: diccionario con los atributos del objeto
        """
        if atributos_excluidos is None:
            atributos_excluidos = []
        columns = [c for c in self.__table__.columns if c.name not in
                   atributos_excluidos]
        return {c.name: getattr(self, c.name) for c in columns}


    @classmethod
    def listar_por_pagina(cls, pagina: int, por_pagina: int) -> dict:
        """Retorna un diccionario con los datos del modelo paginados

        Args:
            pagina (int): numero de pagina
            por_pagina (int): elementos por pagina

        Returns:
            dict: datos paginados del modelo
        """
        paginacion = cls.query.paginate(page=pagina, per_page=por_pagina)
        lista = [item.json() for item in paginacion.items]
        arch = {
            "data": lista,
            "page": paginacion.page,
            "per_page": paginacion.per_page,
            "total": paginacion.total
        }
        return arch

    @classmethod
    def paginar(cls, lista: list, pagina: int, elementos_por_pagina: int) -> dict:
        """pagina todos los objetos que le tires de un modelo

        Args:
            lista list: lista de objetos
            pagina int: pagina requerida
            elementos_por_pagina int: elementos por pagina

        Returns:
            dict: datos paginados de los modelos
        """
        total_elementos = len(lista)
        total_paginas = (total_elementos + elementos_por_pagina - 1) // elementos_por_pagina

        inicio = (pagina - 1) * elementos_por_pagina
        fin = inicio + elementos_por_pagina

        datos_paginados = [solicitud.json() for solicitud in lista[inicio:fin]]

        paginacion = {
            "data": datos_paginados,
            "page": pagina,
            "per_page": elementos_por_pagina,
            "total": total_elementos,
            "total_pages": total_paginas
        }
        return paginacion

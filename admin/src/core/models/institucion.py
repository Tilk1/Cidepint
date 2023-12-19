from src.core.basededatos import db
from src.core.models.usuario import usuario_tiene_rol
from src.core.models.rol import Rol
from src.core.models.base import BaseModel
from src.core.models.usuario import Usuario


class Institucion(BaseModel):
    __tablename__ = "instituciones"
    nombre = db.Column(db.String(255), nullable=False)
    informacion = db.Column(db.String(255))
    direccion = db.Column(db.String(255))
    localizacion = db.Column(db.String(255))
    web = db.Column(db.String(255))
    palabras_clave = db.Column(db.String(255))
    dias_horarios = db.Column(db.String(255))
    info_contacto = db.Column(db.String(255))
    habilitada = db.Column(db.Boolean, default=True)
    servicios = db.relationship('Servicio', backref='instituciones', lazy=True)

    @classmethod
    def listar_por_pagina(cls, pagina, por_pagina, atributos_excluidos=None) -> dict:
        inicio = (pagina - 1) * por_pagina
        fin = inicio + por_pagina
        lista = []
        instituciones = Institucion.query.slice(inicio, fin)
        for institucion in instituciones:
            lista.append(institucion.json(atributos_excluidos))
        arch = {
            "data": lista,
            "page": pagina,
            "per_page": por_pagina,
            "total": Institucion.contar_todos()
        }
        return arch

    def agregar_integrante(self, usuario, rol) -> None:
        """agregar_integrante

        Args:
            usuario (object): usuario a agregar
            rol (object): rol a asignar
        """
        db.session.execute(
            usuario_tiene_rol.insert().values(
                usuario_id=usuario.id,
                rol_id=rol.id,
                institucion_id=self.id
            )
        )
        db.session.commit()

    def obtener_integrantes(self) -> list:
        """obtener_integrantes

        Returns:
            list: retorna una lista de objetos usuarios
        """
        usuarios = db.session.query(Usuario).join(usuario_tiene_rol).filter(
            usuario_tiene_rol.c.institucion_id == self.id).all()
        return usuarios

    def obtener_servicios(self) -> list:
        from src.core.models.servicio import Servicio
        """obtener_servicios

        Returns:
            list: retorna una lista de objetos servicios
        """
        servicios = db.session.query(Servicio).filter(
            Servicio.institucion_id == self.id).all()
        return servicios

    def obtener_rol_usuario(self, usuario: object) -> object:
        """obtener_rol_usuario

        Args:
            usuario (object): usuario a buscar

        Returns:
            object: retorna el rol del usuario
        """
        rol = db.session.query(Rol).join(usuario_tiene_rol).filter(
            usuario_tiene_rol.c.usuario_id == usuario.id,
            usuario_tiene_rol.c.institucion_id == self.id).first()
        return rol

    def contar_integrantes(self) -> int:
        """Contar los integrantes de la institucion

        Returns:
            int: cantidad de integrantes
        """
        return db.session.query(Usuario).join(usuario_tiene_rol).filter(
            usuario_tiene_rol.c.institucion_id == self.id).count()

    def obtener_integrantes_paginados(self, pagina: int, por_pagina: int):
        """Obtener todos los integrantes de la institucion de
           forma paginada

        Args:
            pagina (int): numero de pagina
            por_pagina (int): cantidad de elementos por pagina

        Returns:
            dict: diccionario con los elementos necesarios para paginar
        """
        inicio = (pagina - 1) * por_pagina
        fin = inicio + por_pagina
        lista = []
        integrantes = db.session.query(Usuario).join(usuario_tiene_rol).filter(
            usuario_tiene_rol.c.institucion_id == self.id).slice(inicio, fin)
        for integrante in integrantes:
            lista.append(integrante)
        arch = {
            "data": lista,
            "page": pagina,
            "per_page": por_pagina,
            "total": self.contar_integrantes()
        }
        return arch

    def eliminar_rol_usuario(self, usuario: object):
        """Para eliminar el rol de un usuario dentro de
           una institucion

        Args:
            usuario (object): usuario al que se le borrara el rol
        """
        db.session.query(usuario_tiene_rol).filter(
            usuario_tiene_rol.c.usuario_id == usuario.id,
            usuario_tiene_rol.c.institucion_id == self.id
        ).delete()
        db.session.commit()

    def usuario_es_integrante(self, usuario: object) -> bool:
        """Para saber si el usuario es parte de la institucion

        Args:
            usuario (object): usuario que se quiere
            saber si forma parte de la institucion

        Returns:
            bool: retorna verdadero si es integrante
        """
        existe = db.session.query(usuario_tiene_rol).filter(
            usuario_tiene_rol.c.institucion_id == self.id,
            usuario_tiene_rol.c.usuario_id == usuario.id).count()
        if existe >= 1:
            return True
        return False

    def contar_integrantes_filtrados(self, palabra: str, estado: str) -> int:
        cant_integrantes_buscados = Usuario.query.join(usuario_tiene_rol, Usuario.id == usuario_tiene_rol.c.usuario_id).filter(Usuario.correo.like(f'%{palabra}%'), usuario_tiene_rol.c.institucion_id == self.id).count()
        if estado == "activo":
            cant_integrantes_buscados = Usuario.query.join(usuario_tiene_rol, Usuario.id == usuario_tiene_rol.c.usuario_id).filter(Usuario.correo.like(f'%{palabra}%'), Usuario.activo, usuario_tiene_rol.c.institucion_id == self.id).count()
        elif estado == "noactivo":
            cant_integrantes_buscados = Usuario.query.join(usuario_tiene_rol, Usuario.id == usuario_tiene_rol.c.usuario_id).filter(Usuario.correo.like(f'%{palabra}%'), Usuario.activo == False, usuario_tiene_rol.c.institucion_id == self.id).count()
        return cant_integrantes_buscados

    def listar_filtrado_integrantes(self, pagina, por_pagina, palabra, estado) -> dict:
        """Lista paginadamente los usuarios aplicando los filtros

        Args:
            pagina (int): nro de la pagina
            por_pagina (int): cant de usuarios por pagina
            palabra (str): string a buscar en el correo del usuario
            estado (str): estado del usuario por el que se desea filtrar

        Returns:
            dict: diccionario con los datos necesarios para paginar
        """
        integrantes_buscados = Usuario.query.join(usuario_tiene_rol, Usuario.id == usuario_tiene_rol.c.usuario_id).filter(Usuario.correo.like(f'%{palabra}%'), usuario_tiene_rol.c.institucion_id == self.id).paginate(page=pagina, per_page=por_pagina)
        if estado == "activo":
            integrantes_buscados = Usuario.query.join(usuario_tiene_rol, Usuario.id == usuario_tiene_rol.c.usuario_id).filter(Usuario.correo.like(f'%{palabra}%'), Usuario.activo, usuario_tiene_rol.c.institucion_id == self.id).paginate(page=pagina, per_page=por_pagina)
        elif estado == "noactivo":
            integrantes_buscados = Usuario.query.join(usuario_tiene_rol, Usuario.id == usuario_tiene_rol.c.usuario_id).filter(Usuario.correo.like(f'%{palabra}%'), Usuario.activo == False, usuario_tiene_rol.c.institucion_id == self.id).paginate(page=pagina, per_page=por_pagina)
        lista = [item for item in integrantes_buscados.items]
        total = self.contar_integrantes_filtrados(palabra, estado)
        arch = {
            "data": lista,
            "page": pagina,
            "per_page": por_pagina,
            "total": total
        }
        return arch
    
    def tiempo_de_resolucion_promedio(self):
        """tiempo promedio de resolución de solicitudes 
            de una institución

        Returns:
            float: retorna un float si hay solicitudes finalizadas,
            sino retorna None
        """
        lista = []
        for servicio in self.obtener_servicios():
            tiempo = servicio.obtener_tiempo_promedio_resolucion()
            if tiempo is not None:
                lista.append(tiempo)
        if lista:
            return sum(lista) / len(lista)
        return None
    
    @classmethod
    def obtener_institucion_por_nombre(cls, nombre):
        """obtener una institución por su nombre

        Args:
            nombre (str): nombre de la institución

        Returns:
            json: diccionario con el detalle de la institución 
        """
        return Institucion.query.filter_by(nombre=nombre).first()
    
    @classmethod
    def filtrar_nombres(cls, nombre):
        """busca las instituciones que contengan 
           la cadena

        Args:
            nombre (str): término de busqueda

        Returns:
            list: lista con los ids de las instituciones
            que cpinciden
        """
        instituciones = Institucion.query.filter(
            db.func.lower(Institucion.nombre).like(f"%{nombre.lower()}%"))
        lista = []
        for institucion in instituciones:
            lista.append(institucion.id)
        return lista
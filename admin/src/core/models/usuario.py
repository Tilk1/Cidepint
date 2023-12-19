from datetime import datetime
from src.core.basededatos import db
from src.core.bcrypt import bcrypt
from src.core.models.base import BaseModel
from src.core.models.configuracion import Configuracion
from src.core.models.rol import Rol

usuario_tiene_rol = db.Table(
    "usuario_tiene_rol",
    db.Column("usuario_id", db.Integer,
              db.ForeignKey("usuarios.id", ondelete='CASCADE'),
              primary_key=True),
    db.Column("institucion_id", db.Integer,
              db.ForeignKey("instituciones.id", ondelete='CASCADE'),
              primary_key=True),
    db.Column("rol_id", db.Integer,
              db.ForeignKey("roles.id"),
              primary_key=True),
    extend_existing=True
)


class Usuario(BaseModel):
    __tablename__ = "usuarios"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, unique=True)
    correo = db.Column(db.String(255), unique=True, nullable=False)
    nombre_usuario = db.Column(db.String(255), unique=True)
    contraseña = db.Column(db.String(255))
    activo = db.Column(db.Boolean)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    tipo_documento = db.Column(db.String(255))
    nro_documento = db.Column(db.String(255))
    genero = db.Column(db.String(255))
    genero_otro = db.Column(db.String(255))
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(255))
    es_super_admin = db.Column(db.Boolean, default=False)
    es_cuenta_google = db.Column(db.Boolean, nullable=False)
    creado_el = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_el = db.Column(db.DateTime, default=datetime.utcnow,
                               onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def crear_usuario(cls, usr: dict) -> object:
        """Crea un usuario en la BD (para los seeds)

        Args:
            usr (dict): diccionario con todos los datos del usuario

        Returns:
            object: el usuario que se acaba de crear
        """
        correo = usr.get("correo"),
        nombre = usr.get("nombre"),
        apellido = usr.get("apellido"),
        tipo_documento = usr.get("tipo_documento"),
        nro_documento = usr.get("nro_documento"),
        direccion = usr.get("direccion"),
        genero = usr.get("genero")
        genero_otro = usr.get("genero_otro")
        telefono = usr.get("telefono")
        contraseña = usr.get("contraseña")
        nombre_usuario = usr.get("nombre_usuario")
        activo = usr.get("activo")
        es_super_admin = usr.get("es_super_admin")
        es_cuenta_google = False
        usuario = Usuario(correo=correo, nombre=nombre, apellido=apellido,
                          tipo_documento=tipo_documento, genero=genero,
                          nro_documento=nro_documento, direccion=direccion,
                          telefono=telefono, nombre_usuario=nombre_usuario,
                          genero_otro=genero_otro, activo=activo,
                          es_super_admin=es_super_admin,
                          es_cuenta_google=es_cuenta_google)
        hash = bcrypt.generate_password_hash(contraseña.encode("utf-8"))
        usuario.contraseña = hash.decode("utf-8")
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @classmethod
    def crear_usuario_preregistro(cls, usr: dict) -> object:
        """Crea un usuario con los datos basicos

        Args:
            usr (dict): diccionario con todos los datos del usuario

        Returns:
            object: el usuario que se inserto en la BD
        """
        correo = usr.get("correo")
        nombre = usr.get("nombre"),
        apellido = usr.get("apellido"),
        tipo_documento = usr.get("tipo_documento")
        genero = usr.get("genero")
        genero_otro = usr.get("genero_otro")
        nro_documento = usr.get("nro_documento")
        direccion = usr.get("direccion")
        telefono = usr.get("telefono")
        usuario = Usuario(correo=correo, nombre=nombre, apellido=apellido,
                          tipo_documento=tipo_documento, genero=genero,
                          nro_documento=nro_documento, genero_otro=genero_otro,
                          direccion=direccion, telefono=telefono,
                          es_cuenta_google=False)
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @classmethod
    def buscar_usuario_por_correo(cls, correo: str) -> object:
        """Busca en la BD un usuario a traves del atributo correo

        Args:
            correo (str): correo del usuario

        Returns:
            object: si encuentra el usuario lo retorna, sino se retorna None
        """
        return Usuario.query.filter_by(correo=correo).first()

    @classmethod
    def chequear_contraseña(cls, contraseña: str, contra: str) -> bool:
        """Verifica si el usuario existe en la BD, y si la
           contraseña es correcta

        Args:
            usuario (str): usuario al que se verificara la contraseña
            contraseña (str): contraseña a verificar

        Returns:
            bool: retorna true si la contraseña es la correcta
        """
        return bcrypt.check_password_hash(contraseña, contra.encode("utf-8"))

    @classmethod
    def actualizar_usuario_registro(cls, correo: str, usr: dict) -> object:
        """Inserta en la BD los datos restantes del usuario

        Args:
            correo (str): correo del usuario que realiza el registro
            usr (dict): diccionario con los datos del usuario

        Returns:
            object: el usuario creado
        """
        contraseña = usr["contraseña"]
        nombre_usuario = usr["nombre_usuario"]
        hash = bcrypt.generate_password_hash(contraseña.encode("utf-8"))
        usuario = Usuario.query.filter_by(correo=correo).first()
        usuario.contraseña = hash.decode("utf-8")
        usuario.nombre_usuario = nombre_usuario
        usuario.activo = True
        db.session.commit()
        return usuario

    @classmethod
    def contar_usuarios(cls) -> int:
        """contar

        Returns:
            int: retorna la cantidad de usuarios
        """
        return Usuario.query.count()

    @classmethod
    def obtener_todos(cls) -> list:
        """contar

        Returns:
            int: retorna todos los usuarios
        """
        return Usuario.query.all()

    @classmethod
    def listar_por_pagina(cls, pagina: int, por_pagina: int) -> dict:
        """Lista paginadamente todos los usuarios de la aplicacion

        Args:
            pagina (int): nro de la pagina
            por_pagina (int): cant de usuarios por pagina

        Returns:
            dict: diccionario con los datos necesarios para paginar
        """
        elem_por_pag = Configuracion.get_elementos_por_pagina()
        inicio = (pagina - 1) * por_pagina
        fin = inicio + por_pagina
        lista = []
        usuarios = Usuario.query.slice(inicio, fin)
        for usuario in usuarios:
            lista.append(usuario)
        arch = {
            "data": lista,
            "page": pagina,
            "per_page": elem_por_pag,
            "total": Usuario.contar_todos()
        }
        return arch

    @classmethod
    def modificar_perfil(cls, usr: dict):
        """Modifica los campos del perfil del usuario. Si la contraseña
        cambia, se encarga de hashearna antes de guardarla en la BD

        Args:
            usr (dict): diccionario que contiene los datos del usuario
        """
        usuario = Usuario.buscar_usuario_por_correo(usr["correo"])
        if not usuario.contraseña == usr['contraseña']:
            hash = bcrypt.generate_password_hash(usr['contraseña'].encode("utf-8"))
            usr['contraseña'] = hash.decode("utf-8")
        for clave, valor in usr.items():
            setattr(usuario, clave, valor)
        db.session.commit()

    @classmethod
    def listar_filtrado(cls, pagina, por_pagina, palabra, estado) -> dict:
        """Lista paginadamente los usuarios aplicando los filtros

        Args:
            pagina (int): nro de la pagina
            por_pagina (int): cant de usuarios por pagina
            palabra (str): string a buscar en el correo del usuario
            estado (str): estado del usuario por el que se desea filtrar

        Returns:
            dict: diccionario con los datos necesarios para paginar
        """
        usuarios_buscados = Usuario.query.filter(Usuario.correo.like(f'%{palabra}%')).paginate(page=pagina, per_page=por_pagina)
        if estado == "activo":
            usuarios_buscados = Usuario.query.filter(Usuario.correo.like(f'%{palabra}%'), Usuario.activo).paginate(page=pagina, per_page=por_pagina)
        elif estado == "noactivo":
            usuarios_buscados = Usuario.query.filter(Usuario.correo.like(f'%{palabra}%'), Usuario.activo == False).paginate(page=pagina, per_page=por_pagina)
        lista = [item.json() for item in usuarios_buscados.items]
        total = Usuario.contar_usuarios_filtrados(palabra, estado)
        arch = {
            "data": lista,
            "page": pagina,
            "per_page": por_pagina,
            "total": total
        }
        return arch

    @classmethod
    def contar_usuarios_filtrados(cls, palabra: str, estado: str) -> int:
        """Cuenta la cantidad de usuarios filtrados

        Args:
            palabra (str): string a buscar en el correo del usuario
            estado (str): estado del usuario por el que se desea filtrar

        Returns:
            int: cantidad de usuarios filtrados
        """
        cant_usuarios = Usuario.query.filter(Usuario.correo.like(f'%{palabra}%')).count()
        if estado == "activo":
            cant_usuarios = Usuario.query.filter(Usuario.correo.like(f'%{palabra}%'), Usuario.activo).count()
        elif estado == "noactivo":
            cant_usuarios = Usuario.query.filter(Usuario.correo.like(f'%{palabra}%'), Usuario.activo == False).count()
        return cant_usuarios

    def obtener_instituciones(self):
        from src.core.models.institucion import Institucion
        """obtener_instituciones

        Returns:
            list: retorna todas las instituciones a las que pertenece el
            usuario
        """
        instituciones = db.session.query(Institucion).join(
            usuario_tiene_rol, Institucion.id == usuario_tiene_rol.c.
            institucion_id).filter(
                usuario_tiene_rol.c.usuario_id == self.id).all()
        return instituciones

    def obtener_roles_en_institucion(self, institucion_id: int) -> list:
        """Obtiene los roles que tiene el usuario que invoca la funcion
           en la institucion que se pasa por parametro

        Args:
            institucion_id (int): id de la institucion

        Returns:
            list: resultado de la consulta
        """
        rol_en_institucion = db.session.query(Rol).\
            join(usuario_tiene_rol, Rol.id == usuario_tiene_rol.c.rol_id).\
            filter(usuario_tiene_rol.c.usuario_id == self.id).\
            filter(usuario_tiene_rol.c.institucion_id == institucion_id).all()
        return rol_en_institucion

    def saber_si_es_super_usuario(self):
        """ Retorna el valor del campo es_super_admin
            del usuario que llama la funcion """
        return self.es_super_admin

    def json_perfil_api(self):
        """Obtener información de un usuario

        Returns:
            diccionario: información del perfil de un usuario
        """
        return {
            "user": self.nombre_usuario,
            "email": self.correo,
            "document_type": self.tipo_documento,
            "document_number": self.nro_documento,
            "gender": self.genero,
            "gender_other": self.genero_otro,
            "address": self.direccion,
            "phone": self.telefono
        }

    def obtener_estado(self):
        """Retorna el si el usuario esta activo
           o inactivo"""
        return self.activo

    @classmethod
    def buscar_usuario_por_nombre_usuario(cls, nombre_usuario: str) -> object:
        """Busca en la BD un usuario a traves del atributo nombre_usuario

        Args:
            nombre_usuario (str): nombre de usuario del usuario

        Returns:
            object: si encuentra el usuario lo retorna, sino se retorna None
        """
        return Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()

    @classmethod
    def crear_usuario_google(cls, usr: dict) -> object:
        """Crea un usuario con los datos basicos

        Args:
            usr (dict): diccionario con todos los datos del usuario

        Returns:
            object: el usuario que se inserto en la BD
        """
        correo = usr.get("correo")
        nombre = usr.get("nombre"),
        apellido = usr.get("apellido"),
        tipo_documento = usr.get("tipo_documento")
        genero = usr.get("genero")
        genero_otro = usr.get("genero_otro")
        nro_documento = usr.get("nro_documento")
        direccion = usr.get("direccion")
        telefono = usr.get("telefono")
        nombre_usuario = usr.get("nombre_usuario")
        usuario = Usuario(correo=correo, nombre=nombre, apellido=apellido,
                          tipo_documento=tipo_documento, genero=genero,
                          nro_documento=nro_documento, genero_otro=genero_otro,
                          direccion=direccion, telefono=telefono, activo=True,
                          nombre_usuario=nombre_usuario, es_cuenta_google=True)
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @classmethod
    def modificar_perfil_google(cls, usr: dict):
        """Modifica los campos del perfil del usuario.

        Args:
            usr (dict): diccionario que contiene los datos del usuario
        """
        usuario = Usuario.buscar_usuario_por_correo(usr["correo"])
        for clave, valor in usr.items():
            setattr(usuario, clave, valor)
        db.session.commit()

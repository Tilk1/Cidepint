from src.core.models.permiso import Permiso
from src.core.models.rol import Rol
from src.core.basededatos import db
from src.core.models.usuario import Usuario
from src.core.models.usuario import usuario_tiene_rol
from src.core.models.institucion import Institucion
from sqlalchemy.ext.associationproxy import association_proxy


def run():
    print("Agregando seed de usuario_tiene_rol..")
    try:
        laura = Usuario.query.filter_by(correo="laura@gmail.com").first()
        institucion = Institucion.listar(1)
        institucion2 = Institucion.listar(2)
        rol_admin = Rol.query.filter_by(nombre="Administrador").first()
        rol_dueño = Rol.query.filter_by(nombre="Dueño").first()
        institucion.agregar_integrante(laura, rol_admin)
        institucion2.agregar_integrante(laura, rol_dueño)

    except Exception as e:
        print("Error al agregar seed de usuario_tiene_rol: ", e)
        raise e

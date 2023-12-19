from src.core.models.rol import Rol
from src.core.basededatos import db
from src.web.utils.permisos import definir_permisos


def run():
    print("Agregando seed de roles..")
    try:
        dueño = Rol.crear(nombre="Dueño")
        administrador = Rol.crear(nombre="Administrador")
        operador = Rol.crear(nombre="Operador")

        permisos = definir_permisos()
        dueño.permisos.extend(permisos["dueño"])
        administrador.permisos.extend(permisos["administrador"])
        operador.permisos.extend(permisos["operador"])
        db.session.commit()

    except Exception as e:
        print("Error al agregar seed de roles: ", e)
        raise e

from src.web.seeders import seed_usuario, seed_institucion, seed_servicios
from src.web.seeders import seed_roles, seed_permisos, seed_solicitudes
from src.web.seeders import seed_usuario_tiene_rol, seed_notas
from src.web.seeders import seed_configuracion
from src.core import basededatos


def init_comandos(app):
    @app.cli.command(name="resetdb")
    def resetdb():
        """ Resetea las tablas de la base de datos"""
        basededatos.reset_db()

    @app.cli.command(name="seedsdb")
    def seedsdb():
        """
            Agrega los seeds a la base de datos
        """
        try:
            seed_configuracion.run()
            seed_usuario.run()
            seed_institucion.run()
            seed_servicios.run()
            seed_permisos.run()
            seed_roles.run()
            seed_solicitudes.run()
            seed_usuario_tiene_rol.run()
            seed_notas.run()
        except Exception:
            print("\033[31mError al agregar seeds a la base de datos\033[0m")
        else:
            print("\033[32mSeeds agregados con éxito!\033[0m")

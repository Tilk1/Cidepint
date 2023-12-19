from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def init_db(app):
    """Inicializacion de la base de datos"""
    db.init_app(app)
    config_db(app)


def config_db(app):
    """Cierra la conexion con la base de datos al terminar
        el request que la abrio """
    @app.teardown_request
    def close_session(exception=None):
        db.session.close()


def reset_db():
    """ Elimina las tablas de la base de datos y las vuelve a crear
        Si surge un error en el proceso, se imprime el error """
    try:
        print("Eliminando BD...")
        db.drop_all()
        print("Creando BD...")
        db.create_all()
        print("Se ha reseteado la BD")
    except Exception as e:
        print("Error: ", e)

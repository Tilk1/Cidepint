from flask import Flask
from flask_session import Session
from src.web.controllers import error
from src.core import basededatos
from src.web.config import config
from src.web.controllers.instituciones import instituciones_bp
from web.controllers.usuario import usuario_bp
from web.controllers.autenticacion import autenticacion_bp
from flask_mail import Mail
from src.web.api.api import api_bp
from src.web.controllers.servicios import servicios_bp
from src.web.controllers.solicitudes import solicitud_servicio_bp
from web.controllers.configuracion import configuracion_bp
from src.web.controllers.index import index_bp
from src.web.helpers.autenticacion_helper import esta_auntenticado
from src.web.helpers.permiso_helper import tiene_permiso_front
from src.web.utils.comandos import init_comandos
from src.web.helpers.mantenimiento import verificar_sitio_habilitado
from src.core import oauth_google
from flask_jwt_extended import JWTManager
from flask_cors import CORS

session = Session()
mail = Mail()
jwt = JWTManager()


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    app.json.ensure_ascii = False
    app.register_error_handler(404, error.error_404)
    app.register_error_handler(401, error.error_401)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

    session.init_app(app)
    mail.init_app(app)
    oauth_google.init_app(app)
    jwt.init_app(app)

    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": ["http://localhost:5173", "https://grupo15.proyecto2023.linti.unlp.edu.ar"]}})
    basededatos.init_db(app)

    init_comandos(app)

    app.jinja_env.globals.update(esta_auntenticado=esta_auntenticado)
    app.jinja_env.globals.update(tiene_permiso_front=tiene_permiso_front)

    app.register_blueprint(instituciones_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(servicios_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(autenticacion_bp)
    app.register_blueprint(configuracion_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(solicitud_servicio_bp)

    app.before_request(verificar_sitio_habilitado)
    return app


from src.core.basededatos import db
from src.core.models.base import BaseModel


class Configuracion(BaseModel):
    elementos_por_pagina = db.Column(db.Integer, default=5)
    info_contacto = db.Column(db.String(255), default='Info por defecto')
    mensaje_mantenimiento = db.Column(db.String(255), default='Mensaje por defecto')
    sitio_habilitado = db.Column(db.Boolean, default=True)

    @classmethod
    def get_configuracion(cls):
        return ConfigManager.obtener_configuracion()

    @classmethod
    def get_elementos_por_pagina(cls):
        return ConfigManager.obtener_configuracion().elementos_por_pagina

    @classmethod
    def get_mensaje_mantenimiento(cls):
        return ConfigManager.obtener_configuracion().mensaje_mantenimiento

    @classmethod
    def get_info_contacto(cls):
        return ConfigManager.obtener_configuracion().info_contacto

    @classmethod
    def get_sitio_habilitado(cls):
        return ConfigManager.obtener_configuracion().sitio_habilitado

    def modificar(self, **kwargs) -> None:
        """Modificar el objeto con nuevos valores y guardarlo en la db

        Params:
            kwargs: atributos del objeto a modificar

        Returns:
            None
        """
        for key, value in kwargs.items():
            if hasattr(ConfigManager.obtener_configuracion(), key) and value is not None:
                setattr(ConfigManager.obtener_configuracion(), key, value)
        if int(ConfigManager.obtener_configuracion().elementos_por_pagina) < 1:
            ConfigManager.obtener_configuracion().elementos_por_pagina = 1
            raise Exception('El numero de elementos por pagina debe ser mayor a 0')
        db.session.commit()


class ConfigManager:
    _instancia = None

    @classmethod
    def obtener_configuracion(cls):
        """Obtiene la unica instacia de configuracion.
        Es un singleton

        Returns:
            Configuracion: Instancia de configuracion
        """
        if cls._instancia is None:
            cls._instancia = db.session.query(Configuracion).first()
            if cls._instancia is None:
                cls._instancia = Configuracion.crear()
        return cls._instancia

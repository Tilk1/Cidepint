from src.core.models.permiso import Permiso


def definir_permisos():
    permisos = {

        "dueño": [
            # Modulo administracion usuarios de institucion
            Permiso.listar_por_nombre("admin_usuarios_institucion_index"),
            Permiso.listar_por_nombre("admin_usuarios_institucion_create"),
            Permiso.listar_por_nombre("admin_usuarios_institucion_destroy"),
            Permiso.listar_por_nombre("admin_usuarios_institucion_update"),
            # Modulo administracion de servicio
            Permiso.listar_por_nombre("admin_servicios_index"),
            Permiso.listar_por_nombre("admin_servicios_show"),
            Permiso.listar_por_nombre("admin_servicios_update"),
            Permiso.listar_por_nombre("admin_servicios_create"),
            Permiso.listar_por_nombre("admin_servicios_destroy"),
            # Modulo de gestion de solicitud servicio
            Permiso.listar_por_nombre("solicitud_servicios_index"),
            Permiso.listar_por_nombre("solicitud_servicios_show"),
            Permiso.listar_por_nombre("solicitud_servicios_update"),
            Permiso.listar_por_nombre("solicitud_servicios_destroy")
        ],

        "administrador": [
            # Modulo administracion de servicio
            Permiso.listar_por_nombre("admin_servicios_index"),
            Permiso.listar_por_nombre("admin_servicios_show"),
            Permiso.listar_por_nombre("admin_servicios_update"),
            Permiso.listar_por_nombre("admin_servicios_create"),
            Permiso.listar_por_nombre("admin_servicios_destroy"),
            # Modulo gestion de solicitud servicio
            Permiso.listar_por_nombre("solicitud_servicios_index"),
            Permiso.listar_por_nombre("solicitud_servicios_show"),
            Permiso.listar_por_nombre("solicitud_servicios_update"),
            Permiso.listar_por_nombre("solicitud_servicios_destroy")
        ],

        "operador": [
            # Modulo administracion de servicio
            Permiso.listar_por_nombre("admin_servicios_index"),
            Permiso.listar_por_nombre("admin_servicios_show"),
            Permiso.listar_por_nombre("admin_servicios_update"),
            Permiso.listar_por_nombre("admin_servicios_create"),
            # Modulo gestion de solicitud servicio
            Permiso.listar_por_nombre("solicitud_servicios_index"),
            Permiso.listar_por_nombre("solicitud_servicios_show"),
            Permiso.listar_por_nombre("solicitud_servicios_update")
        ]
    }

    return permisos

from src.core.models.permiso import Permiso


def run():
    print("Agregando seed de permisos..")
    try:
        ###############################
        ### Permisos modulo usuario ###
        ###############################
        Permiso.crear(nombre="user_index")
        Permiso.crear(nombre="user_show")
        Permiso.crear(nombre="user_new")
        Permiso.crear(nombre="user_update")
        Permiso.crear(nombre="user_destroy")

        ###################################
        ### Administracion institucion  ###
        ###################################
        Permiso.crear(nombre="admin_institucion_index")
        Permiso.crear(nombre="admin_institucion_show")
        Permiso.crear(nombre="admin_institucion_update")
        Permiso.crear(nombre="admin_institucion_create")
        Permiso.crear(nombre="admin_institucion_destroy")
        Permiso.crear(nombre="admin_institucion_activate")
        Permiso.crear(nombre="admin_institucion_deactivate")

        #################################################
        ### Adminsitracion usuarios de la institucion ###
        #################################################
        Permiso.crear(nombre="admin_usuarios_institucion_index")
        Permiso.crear(nombre="admin_usuarios_institucion_create")
        Permiso.crear(nombre="admin_usuarios_institucion_destroy")
        Permiso.crear(nombre="admin_usuarios_institucion_update")

        ###########################################
        ###     Administracion de servicios     ###
        ###########################################
        Permiso.crear(nombre="admin_servicios_index")
        Permiso.crear(nombre="admin_servicios_show")
        Permiso.crear(nombre="admin_servicios_update")
        Permiso.crear(nombre="admin_servicios_create")
        Permiso.crear(nombre="admin_servicios_destroy")

        ###########################################
        ### Gestion de solicitud de servicio    ###
        ###########################################
        Permiso.crear(nombre="solicitud_servicios_index")
        Permiso.crear(nombre="solicitud_servicios_show")
        Permiso.crear(nombre="solicitud_servicios_update")
        Permiso.crear(nombre="solicitud_servicios_destroy")

        ###########################################
        ###          Configuracion              ###
        ###########################################
        Permiso.crear(nombre="configuracion_show")
        Permiso.crear(nombre="configuracion_update")

    except Exception as e:
        print("Error al agregar seed de permisos: ", e)
        raise e

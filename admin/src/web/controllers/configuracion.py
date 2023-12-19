from flask import Blueprint, render_template, flash, request, redirect, url_for
from src.core.models.configuracion import Configuracion
from src.web.helpers.permiso_helper import tiene_permiso
from src.web.helpers.autenticacion_helper import inicio_sesion_requerido

# Crear un Blueprint
configuracion_bp = Blueprint('configuracion', __name__, url_prefix='/configuracion')


@configuracion_bp.get('/')
@inicio_sesion_requerido
@tiene_permiso()
def index():
    config = Configuracion.get_configuracion()
    return render_template('configuracion.html', data=config)


@configuracion_bp.post('/')
@inicio_sesion_requerido
@tiene_permiso()
def actualizar_configuracion():
    config = Configuracion.get_configuracion()
    if config is None:
        config = Configuracion.crear()
    accion = request.form.get('accion')
    if accion == 'guardar':
        try:
            config.modificar(
                elementos_por_pagina=int(request.form['elementos_por_pagina']),
                info_contacto=request.form['info_contacto'],
                mensaje_mantenimiento=request.form['mensaje_mantenimiento']
            )
        except Exception as e:
            flash('Configuracion fallida '+str(e), 'danger')
        else:
            flash('Configuracion actualizada con exito', 'success')
        finally:
            return redirect(url_for('configuracion.index'))

    elif accion == 'deshabilitar':
        try:
            config.modificar(sitio_habilitado=not(config.sitio_habilitado))
        except Exception as e:
            flash('Configuracion fallida '+str(e), 'danger')
        else:
            flash('Configuracion actualizada con exito', 'success')
        finally:
            return redirect(url_for('index.home'))

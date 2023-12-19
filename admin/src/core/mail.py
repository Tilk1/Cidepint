from flask_mail import Mail, Message
from flask import flash, render_template

mail = Mail()


def init_app(app):
    mail.init_app(app)


def mandar_mensaje_registro(usr: dict, token: str) -> bool:
    """Manda un correo al usuario que realiza el preregistro

    Args:
        usr (dict): info del usuario que contiene el nombre y el correo
        token (str): token creado para ese usuario

    Returns:
        bool: indica si se envio o no el correo
    """
    nombre = usr["nombre"]
    correo = usr["correo"]
    try:
        mensaje = Message("Nueva cuenta en CIDEPINT",
                          sender="noreply@demo.com", recipients=[correo])
        mensaje.html = render_template("usuario/mail.html", nombre=nombre,
                                       token=token)
        mail.send(mensaje)
        return True
    except Exception:
        flash("Error al enviar el correo", "danger")
        return False

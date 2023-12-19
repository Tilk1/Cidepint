from src.core.models.nota_solicitud import NotaSolicitud
from src.core.models.solicitud_servicio import SolicitudServicio
from src.core.models.solicitud_servicio import EstadoEnum as estado
from faker import Faker
import random


def run():
    print("Agregando seed de solicitudes de servicios..")
    fake = Faker('es_ES')
    estados_posibles = [estado.EN_PROCESO, estado.ACEPTADA, estado.RECHAZADA,
                        estado.FINALIZADA, estado.CANCELADA]
    SolicitudServicio.crear(
        titulo="solicitud nro 1",
        servicio_id=1,
        usuario_id=2,
        detalle="soy laura y hice esta solicitud",
        archivos_adjuntos=fake.image_url(),
        estado=estado.ACEPTADA,
        cerrada_el=None
    )
    for i in range(2, 10):
        try:
            SolicitudServicio.crear(
                titulo="solicitud nro " + str(i),
                servicio_id=random.randint(10, 19),
                usuario_id=random.randint(1, 5),
                detalle="detalle de la solicitud nro " + str(i),
                archivos_adjuntos=fake.image_url(),
                estado=random.choice(estados_posibles),
                cerrada_el=None
            )
        except Exception as e:
            print("Error al agregar seed de solicitudes de servicios: ", e)
            raise

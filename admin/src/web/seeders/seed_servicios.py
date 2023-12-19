from src.core.models.servicio import Servicio
from src.core.models.institucion import Institucion
from src.web.seeders import seed_institucion


def run():
    print("Agregando seed de servicios..")
    try:
        for i in range(1, 15):
            servicio = Servicio.crear(
                nombre='servicio'+str(i),
                descripcion='descripcion del servicio',
                palabras_claves='recubrimiento,pintura,latex,esmalte',
                tipo='Análisis',
                habilitado=True,
                institucion_id=1
            )
        for k in range(16, 21):
            servicio = Servicio.crear(
                nombre='servicio'+str(k),
                descripcion='descripcion del servicio',
                palabras_claves='recubrimiento,pintura,latex,esmalte',
                tipo='Desarrollo',
                habilitado=True,
                institucion_id=2
            )
    except Exception as e:
        print("Error al agregar seed de usuarios: ", e)
        raise e

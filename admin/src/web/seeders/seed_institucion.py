from src.core.models.institucion import Institucion
from faker import Faker


def run():
    print("Agregando seed de instituciones..")
    fake = Faker('es_AR')
    try:
        Institucion.crear(
            nombre="Villalba Inc Inc",
            informacion="Dto. 2",
            direccion="Avenida Malvinas Argentinas N° 743\nRawson 9103, Chubut",
            localizacion="-89.958903",
            web="https://www.diaz.org/",
            palabras_clave="et, libero, dolorum",
            dias_horarios="lunes",
            info_contacto="+54 9 3574 1316",
        )
        Institucion.crear(
            nombre="Acosta-Gonzalez Group",
            informacion="Torre 1 Dto. 9",
            direccion="Av. Viedma N° 672 Oficina 72\nNeuquén 8300, Neuquén",
            localizacion="-97.834994",
            web="https://martinez.ar/",
            palabras_clave="et, libero, dolorum",
            dias_horarios="sábado",
            info_contacto="+54 9 3728 8226",
        )
        for i in range(1, 28):
            Institucion.crear(
                nombre=fake.company()+" "+fake.company_suffix(),
                informacion=fake.secondary_address(),
                direccion=fake.address(),
                localizacion=fake.coordinate(),
                web=fake.url(),
                palabras_clave=(fake.word()+", "+fake.word()+", " +
                                fake.word()),
                dias_horarios=fake.day_of_week(),
                info_contacto=fake.phone_number(),
            )
    except Exception as e:
        print("Error al agregar seed de instituciones: ", e)
        raise e

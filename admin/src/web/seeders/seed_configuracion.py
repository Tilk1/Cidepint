from src.core.models.configuracion import Configuracion


def run():
    print("Agregando seed de configuracion..")
    try:
        Configuracion.crear()
    except Exception as e:
        print("Error al agregar seed de configuracion: ", e)
        raise e

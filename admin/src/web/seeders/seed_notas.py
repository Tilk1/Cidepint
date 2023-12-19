from src.core.models.nota_solicitud import NotaSolicitud
import random

notas_posibles = [
    "tukson cosmico",
    "hola me gusta la radio",
    "quisiera...el..servicio.. gracias.."
]

def run():
    print("Agregando seed de notas..")
    try:
        for i in range(1, 5):
            NotaSolicitud.crear(
                usuario_id=i+1,  # evita super_usuario
                solicitud_id=i,
                nota=random.choice(notas_posibles)
            )
    except Exception as e:
        print("Error al agregar seed de usuarios: ", e)
        raise e
from src.core.models.usuario import Usuario
from faker import Faker


def run():
    print("Agregando seed de usuarios..")
    faker = Faker('es')
    try:
        Usuario.crear_usuario(usr={
                "correo": "superAdmin@gmail.com",
                "nombre_usuario": "superAdministrador",
                "contraseña": "admin",
                "activo": True,
                "nombre": "super",
                "apellido": "admin",
                "tipo_documento": "dni",
                "nro_documento": "12345",
                "genero": "F",
                "genero_otro": "F",
                "direccion": "55 y 53",
                "telefono": "221-2131-412",
                "es_super_admin": True
            }
        )
        Usuario.crear_usuario(usr={
                "correo": "laura@gmail.com",
                "nombre_usuario": "laurita555",
                "contraseña": "12345",
                "activo": True,
                "nombre": "Laura",
                "apellido": "Fava",
                "tipo_documento": "dni",
                "nro_documento": "45345345",
                "genero": "F",
                "genero_otro": "F",
                "direccion": "55 y 53",
                "telefono": "221-2131-412",
                "es_super_admin": False
            }
        )
        Usuario.crear_usuario(usr={
                "correo": "jorge@gmail.com",
                "nombre_usuario": "jorgito",
                "contraseña": "12345",
                "activo": True,
                "nombre": "Jorge",
                "apellido": "Runco",
                "tipo_documento": "enrolamiento",
                "nro_documento": "1234567",
                "genero": "M",
                "genero_otro": "M",
                "direccion": "1 y 32",
                "telefono": "221-2131-412",
                "es_super_admin": False
            }
        )
        for i in range(1, 15):
            perfil = faker.simple_profile()
            Usuario.crear_usuario(usr={
                    "correo": perfil['mail'],
                    "nombre_usuario": perfil['username'],
                    "contraseña": "12345",
                    "activo": True,
                    "nombre": perfil['name'],
                    "apellido": faker.last_name(),
                    "tipo_documento": "dni",
                    "nro_documento": "1234567",
                    "genero": perfil['sex'],
                    "genero_otro": perfil['sex'],
                    "direccion": perfil['address'],
                    "telefono": "221-2131-412",
                    "es_super_admin": False
                }
            )

    except Exception as e:
        print("Error al agregar seed de usuarios: ", e)
        raise e

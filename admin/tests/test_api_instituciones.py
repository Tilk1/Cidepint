from web import create_app
import json

app = create_app()
app.testing = True
client = app.test_client()


def validate_parameters(response, expected_error_message):
    assert response.status_code == 400, "Fallo en parametros invalidos"
    response_data = json.loads(response.data)
    assert response_data == expected_error_message, "Fallo en parametros invalidos"


def test_valid_parameters_institutions_1_page():
    response = client.get('/api/institutions?page=1&per_page=1')
    assert response.status_code == 200, "Fallo en la API institutions"
    response_data = json.loads(response.data)
    expected_response = {
        "data": [
            {
                "dias_horarios": "lunes",
                "direccion": "Avenida Malvinas Argentinas N° 743\nRawson 9103, Chubut",
                "habilitada": True,
                "info_contacto": "+54 9 3574 1316",
                "informacion": "Dto. 2",
                "localizacion": "-89.958903",
                "nombre": "Villalba Inc Inc",
                "web": "https://www.diaz.org/"
            }
        ],
        "page": 1,
        "per_page": 1,
        "total": 29
    }
    assert response_data == expected_response, "Fallo en institucion 1/1"

def test_valid_parameters_institutions_2_page():
    response = client.get('/api/institutions?page=1&per_page=2')
    assert response.status_code == 200, "Fallo en la API institutions"
    response_data = json.loads(response.data)
    expected_response = {
        "data": [
            {
                "dias_horarios": "lunes",
                "direccion": "Avenida Malvinas Argentinas N° 743\nRawson 9103, Chubut",
                "habilitada": True,
                "info_contacto": "+54 9 3574 1316",
                "informacion": "Dto. 2",
                "localizacion": "-89.958903",
                "nombre": "Villalba Inc Inc",
                "web": "https://www.diaz.org/"
            },
            {
                "dias_horarios": "sábado",
                "direccion": "Av. Viedma N° 672 Oficina 72\nNeuquén 8300, Neuquén",
                "habilitada": True,
                "info_contacto": "+54 9 3728 8226",
                "informacion": "Torre 1 Dto. 9",
                "localizacion": "-97.834994",
                "nombre": "Acosta-Gonzalez Group",
                "web": "https://martinez.ar/"
            }
        ],
        "page": 1,
        "per_page": 2,
        "total": 29
    }
    assert response_data == expected_response, "Fallo en institucion 1/1"

def test_invalid_parameters_institutions():
    response = client.get('/api/institutions?page=AAAA&per_page=1')
    validate_parameters(response, {"error": "Parámetros inválidos"})

    response = client.get('/api/institutions?page=1&per_page=AAAA')
    validate_parameters(response, {"error": "Parámetros inválidos"})
from web import create_app
import json
from src.core.models.solicitud_servicio import SolicitudServicio

app = create_app()
app.testing = True
client = app.test_client()


def test_obtener_solicitud_servicio():
    headers = {
        "Authorization": "2"  # Laura
    }
    response = client.get('/api/me/requests/1', headers=headers)
    assert response.status_code == 200, "Fallo en API servicios"
    response_data = json.loads(response.data)
    expected_response = {
        "cerrada_el": None,
        "detalle": "soy laura y hice esta solicitud",
        "estado": "Aceptada",
        "titulo": "solicitud nro 1"
    }
    assert response_data["cerrada_el"] == expected_response["cerrada_el"]
    assert response_data["detalle"] == expected_response["detalle"]
    assert response_data["estado"] == expected_response["estado"]
    assert response_data["titulo"] == expected_response["titulo"]
    assert "creado_el" in response_data, "respuesta no tiene creado_el"

def test_obtener_solicitud_servicio_inexistente():
    headers = {
        "Authorization": "2"  # Laura
    }
    response = client.get('/api/me/requests/999999', headers=headers)
    assert response.status_code == 404, "Fallo en API servicios"

def test_cargar_solicitud():
    headers = {
        "Authorization": "2"  # Laura
    }
    body = {
        "titulo": "a long description",
        "descripcion": "a long description",
        "servicio": "1"
    }
    response = client.post('/api/me/requests', headers=headers, json=body)
    assert response.status_code == 201, "Fallo en carga de solicitud"
    solicitud_id = json.loads(response.data)["id"]
    with app.app_context():
        solicitud_en_db = SolicitudServicio.listar(solicitud_id)
    assert solicitud_en_db is not None, "La solicitud no fue creada en la db"


def test_cargar_nota_y_chequear_existencia():
    headers = {
        "Authorization": "2"  # Laura
    }
    body = {
        "nota": "a long description"
    }
    response = client.post('/api/me/requests/1/notes', headers=headers, json=body)
    assert response.status_code == 201, "Fallo en carga de nota"
    nota_id = json.loads(response.data)["id"]
    with app.app_context():
        nota_en_db = SolicitudServicio.listar(nota_id)
    assert nota_en_db is not None, "La nota no fue creada en la db"


def test_api_auth_fail():
    headers = {
        "Authorization": "ASDASASD111"
    }
    response = client.get('/api/me/requests/1', headers=headers)
    assert response.status_code == 401, "Fallo en la API auth"

def test_api_get_solicitud_parametros_invalidos():
    headers = {
        "Authorization": "2"  # Laura
    }
    response = client.get('/api/me/requests/INVALIDOOO', headers=headers)
    assert response.status_code == 400, "Fallo en API servicios"

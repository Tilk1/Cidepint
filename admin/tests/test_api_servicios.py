from web import create_app
import json
from src.core.models.servicio import Servicio

app = create_app()
app.testing = True
client = app.test_client()

def validate_parameters(response, expected_error_message):
    assert response.status_code == 400, "Fallo en parametros invalidos"
    response_data = json.loads(response.data)
    assert response_data == expected_error_message, "Fallo en parametros invalidos"

# def test_invalid_parameters_servicios():
#     response = client.get('/api/services/search?')
#     validate_parameters(response, {"error": "Parámetros inválidos"})

#     response = client.get('/api/services/search?q=algo&page=mal')
#     validate_parameters(response, {"error": "Parámetros inválidos"})

#     response = client.get('/api/services/search?q=algo&per_page=mal')
#     validate_parameters(response, {"error": "Parámetros inválidos"})

def test_listar_servicio():
    response = client.get('/api/services/1')
    assert response.status_code == 200, "Fallo en API servicios"
    response_data = json.loads(response.data)
    expected_response = {
        "descripcion": "descripcion del servicio",
        "habilitado": True,
        "nombre": "servicio1",
        "palabras_claves": "recubrimiento,pintura,latex,esmalte"
    }
    assert response_data["descripcion"] == expected_response["descripcion"]
    assert response_data["habilitado"] == expected_response["habilitado"]
    assert response_data["nombre"] == expected_response["nombre"]
    assert response_data["palabras_claves"] == expected_response["palabras_claves"]
    assert "institucion" in response_data, "falta campo institucion"

def test_listar_servicio_paginado_vacio():
    response = client.get('/api/services/search?q=nadaaaaaaa')
    assert response.status_code == 200, "Fallo en API servicios"
    response_data = json.loads(response.data)
    expected_response = {
            "data": [],
            "page": 1,
            "per_page": 10,
            "total": 0
    }
    assert response_data["data"] == expected_response["data"]

def test_listar_servicio_paginado_1():
    response = client.get('/api/services/search?q=servicio&type=Análisis')
    assert response.status_code == 200, "Fallo en API servicios"
    


    
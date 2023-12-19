from web import create_app
import json
from src.core.models.servicio import Servicio

app = create_app()
app.testing = True
client = app.test_client()


def test_listar_tipos_de_servicio():
    response = client.get('/api/services-types')
    assert response.status_code == 200, "Fallo en API tipos servicios"
    response_data = json.loads(response.data)
    expected_response = Servicio.obtener_tipos()
    assert response_data == expected_response, "Tipos de servicios invalidos"

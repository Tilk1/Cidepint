from web import create_app
import json

app = create_app()
app.testing = True
client = app.test_client()


def test_api_auth():
    headers = {
        "Authorization": "1"
    }
    response = client.post('/api/auth', headers=headers)
    assert response.status_code == 200, "Fallo en la API auth"
    response_data = json.loads(response.data)
    expected_response = {
        "id": "1",
        "resultado": "exito"
    }
    assert response_data == expected_response, "Fallo en datos de auth"


def test_api_auth_fail():
    headers = {
        "Authorization": "ASDASASD111"
    }
    response = client.post('/api/auth', headers=headers)
    assert response.status_code == 401, "Fallo en la API auth"

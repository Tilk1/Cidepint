from web import create_app
from flask import session
import json

app = create_app()
app.testing = True
client = app.test_client()

def test_perfil():
    headers = {
        "Authorization": "2"
    }
    response = client.get('/api/me/profile', headers=headers)
    assert response.status_code == 200, "Fallo en la API profile"
    response_data = json.loads(response.data)
    expected_response = {
        "address": "55 y 53",
        "document_number": "45345345",
        "document_type": "dni",
        "email": "laura@gmail.com",
        "gender": "F",
        "gender_other": "F",
        "phone": "221-2131-412",
        "user": "laurita555",
    }
    assert response_data == expected_response, "Fallo en datos profile"

    headers = {
        "Authorization": "ASDASASD111"
    }
    response = client.post('/api/auth', headers=headers)
    assert response.status_code == 401, "Fallo en la API auth"


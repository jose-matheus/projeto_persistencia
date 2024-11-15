from fastapi.testclient import TestClient
from app import app  # Importe sua aplicação FastAPI

client = TestClient(app)

def test_criar_paciente():
    paciente_data = {
        "nome": "João Silva",
        "data_nascimento": "1990-05-20",
        "telefone": "999999999",
        "endereco": "Rua Exemplo, 123",
        "email": "joao.silva@email.com",
        "cpf": "12345678901",
        "historico_medico": ["Alergia a penicilina"],
        "status": True
    }
    
    response = client.post("/pacientes/", json=paciente_data)

    assert response.status_code == 200
    assert response.json()["nome"] == "João Silva"

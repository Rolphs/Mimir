from fastapi.testclient import TestClient

from ecosistema_ia.api.servidor import app
from ecosistema_ia.sps.mappings import (
    CROMOTIPO_COLOR,
    RITMO_TIPOGRAFIA,
    ARQUETIPO_ICONO,
    ESTILO_ANIMACION,
)

client = TestClient(app)


def test_profile_to_code_roundtrip():
    token = {
        "cromotipo": "sol",
        "ritmo_cognitivo": "lento",
        "arquetipo_narrativo": "explorador",
        "estilo_perceptual": "visual",
    }
    response = client.post("/sps/code", json=token)
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {"styles", "css", "react"}

    styles = data["styles"]
    assert styles["color_primario"] == CROMOTIPO_COLOR[token["cromotipo"]]
    assert styles["fuente_base"] == RITMO_TIPOGRAFIA[token["ritmo_cognitivo"]]
    assert styles["icono"] == ARQUETIPO_ICONO[token["arquetipo_narrativo"]]
    assert styles["animacion"] == ESTILO_ANIMACION[token["estilo_perceptual"]]

    assert styles["color_primario"] in data["css"]
    assert styles["fuente_base"] in data["css"]
    assert styles["icono"] in data["react"]
    assert styles["animacion"] in data["react"]

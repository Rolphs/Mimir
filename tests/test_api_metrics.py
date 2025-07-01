from fastapi.testclient import TestClient
from ecosistema_ia.api.servidor import app
from ecosistema_ia.api.endpoints import territorio
from ecosistema_ia.main import ejecutar_ciclo
from ecosistema_ia.agentes.tipos.herbivoros.herbivoro import Herbivoro


def _herbivoro(id_):
    h = Herbivoro(id_, 0, 0, 0)
    h.memoria.append({"dato": "x"})
    return h


def test_metrics_latest_contains_fields():
    territorio.historial_estados = []
    agentes = [_herbivoro("H1"), _herbivoro("H2")]
    agentes = ejecutar_ciclo(agentes, territorio)
    territorio.regular(agentes, ciclo=1)

    client = TestClient(app)
    response = client.get("/metrics/latest")
    assert response.status_code == 200
    data = response.json()
    assert "densidad" in data
    assert "diversidad" in data
    assert "tension" in data

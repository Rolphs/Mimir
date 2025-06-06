from fastapi.testclient import TestClient
from ecosistema_ia.api.servidor import app

client = TestClient(app)


def test_get_datasets_not_empty():
    response = client.get("/datasets")
    assert response.status_code == 200
    data = response.json()
    assert "datasets" in data
    datasets = data["datasets"]
    assert isinstance(datasets, list)
    assert len(datasets) > 0


def test_preview_has_expected_rows():
    # obtain one existing dataset name
    datasets = client.get("/datasets").json()["datasets"]
    name = datasets[0]["archivo"]
    n = 3
    response = client.get("/datasets/preview", params={"name": name, "n": n})
    assert response.status_code == 200
    data = response.json()
    assert "preview" in data
    preview = data["preview"]
    assert isinstance(preview, list)
    assert len(preview) == n + 1

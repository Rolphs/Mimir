import pytest

from ecosistema_ia.entorno.territorio import Territorio
from ecosistema_ia.agentes.tipos.testing.dummy_agents import DummyA, DummyB


def test_cargar_datasets_not_empty():
    territorio = Territorio()
    assert len(territorio.csvs) > 0
    assert all(p.suffix == ".csv" for p in territorio.csvs)


def test_predicciones_en_estado_json():
    territorio = Territorio()
    agentes = [DummyA(f"A{i}", 0, 0, 0) for i in range(5)] + [DummyB(f"B{i}", 0, 0, 0) for i in range(6)]
    for ciclo in range(6):
        agentes = territorio.regular(agentes, ciclo=ciclo)
    estado = territorio.get_estado_json()
    assert "pred_densidad" in estado
    assert "pred_diversidad" in estado
    assert "pred_tension" in estado

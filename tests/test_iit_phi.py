import ecosistema_ia.metrics.iit_phi as phi
from ecosistema_ia.entorno.territorio import Territorio
from ecosistema_ia.agentes.tipos.testing.dummy_agents import DummyA


def test_phi_connected_cluster():
    agents = [DummyA("A1", 0, 0, 0), DummyA("A2", 1, 0, 0)]
    result = phi.calculate_phi_for_agent_cluster(agents)
    assert result["phi"] == 1.0


def test_phi_disconnected_cluster():
    agents = [DummyA("A1", 0, 0, 0), DummyA("A2", 5, 5, 0)]
    result = phi.calculate_phi_for_agent_cluster(agents)
    assert result["phi"] == 0.0


def test_calcular_metricas_includes_phi():
    territorio = Territorio()
    agents = [DummyA("A1", 0, 0, 0), DummyA("A2", 0, 1, 0)]
    metricas = territorio.calcular_metricas(agents)
    assert "phi" in metricas
    assert metricas["phi"] == 1.0

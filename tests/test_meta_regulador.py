from ecosistema_ia.entorno.meta_regulador import MetaRegulador
from ecosistema_ia.agentes.tipos.testing.dummy_agents import DummyA


class DummyTerritorio:
    def __init__(self, metricas):
        self.metricas = metricas
        self.buzon_mensajes = []
        self.csvs = ["a.csv"]

    def get_csv(self, z):
        return []

    def calcular_metricas(self, agentes):
        return self.metricas


def test_meta_regulador_activa_perturbacion():
    territorio = DummyTerritorio({"densidad": 0.5, "diversidad": 12, "tension": 0.5})
    mr = MetaRegulador(ventana=2, variacion_min=0.001)
    agentes = [DummyA("D-1", 0, 0, 0)]
    mr.evaluar(territorio, agentes)
    mr.evaluar(territorio, agentes)
    assert mr.acciones > 0


def test_meta_regulador_no_actua_si_varia():
    territorio = DummyTerritorio({"densidad": 0.1, "diversidad": 1, "tension": 0.1})
    mr = MetaRegulador(ventana=2, variacion_min=0.001)
    agentes = [DummyA("D-1", 0, 0, 0)]
    mr.evaluar(territorio, agentes)
    territorio.metricas = {"densidad": 0.9, "diversidad": 20, "tension": 0.9}
    mr.evaluar(territorio, agentes)
    assert mr.acciones == 0

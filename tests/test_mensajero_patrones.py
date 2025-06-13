from ecosistema_ia.agentes.tipos.sublimes.mensajero import Mensajero

class DummyTerritorio:
    def __init__(self):
        self.buzon_mensajes = []
        self.llamadas = []
    def desmontar_patron(self, tipo, valor):
        self.llamadas.append((tipo, valor))


def _mensaje(emisor="A", pos=(0,0,0), tipo="info"):
    x, y, z = pos
    return {"emisor": emisor, "x": x, "y": y, "z": z, "tipo": tipo, "dato_util": "d"}


def test_patron_se_desmonta_superado_umbral():
    t = DummyTerritorio()
    m = Mensajero(umbral_patrones=2)
    for ciclo in range(3):
        t.buzon_mensajes = [_mensaje()]
        m.observar(t, [], ciclo)
    assert ("emisor", "A") in t.llamadas


def test_patron_no_desmonta_si_no_supera_umbral():
    t = DummyTerritorio()
    m = Mensajero(umbral_patrones=3)
    for ciclo in range(2):
        t.buzon_mensajes = [_mensaje()]
        m.observar(t, [], ciclo)
    assert t.llamadas == []

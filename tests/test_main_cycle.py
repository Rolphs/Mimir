from ecosistema_ia.main import ejecutar_ciclo
from ecosistema_ia.entorno.territorio import Territorio
from ecosistema_ia.agentes.tipos.carnivoros.divisor_reproductor import (
    DivisorReproductor,
)
from ecosistema_ia.agentes.tipos.carnivoros.destructor import Destructor
from ecosistema_ia.agentes.tipos.herbivoros.herbivoro import Herbivoro


def _herbivoro(id_):
    h = Herbivoro(id_, 0, 0, 0)
    h.memoria.append({"dato": "x"})
    return h


def test_ejecutar_ciclo_agrega_agentes():
    territorio = Territorio()
    dr = DivisorReproductor("DR-001", 0, 0, 0)
    agentes = [dr] + [_herbivoro(f"H{i}") for i in range(4)]
    cantidad_inicial = len(agentes)

    agentes = ejecutar_ciclo(agentes, territorio)

    assert len(agentes) == cantidad_inicial + 1


def test_ejecutar_ciclo_elimina_agentes():
    territorio = Territorio()
    dest = Destructor("D-001", 0, 0, 0)
    rojo = Herbivoro("HR-1", 0, 0, 0)
    rojo.calificacion = "roja"
    rojo.memoria = []
    agentes = [dest, rojo]

    agentes = ejecutar_ciclo(agentes, territorio)

    ids = [a.identificador for a in agentes]
    assert "HR-1" not in ids
    assert "D-001" in ids


def test_metricas_en_estado_json():
    territorio = Territorio()
    agentes = [_herbivoro("H1"), _herbivoro("H2")]
    agentes = ejecutar_ciclo(agentes, territorio)
    territorio.regular(agentes, ciclo=1)
    estado = territorio.get_estado_json()
    assert "densidad" in estado
    assert "diversidad" in estado
    assert "tension" in estado

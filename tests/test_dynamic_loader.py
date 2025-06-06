import re
from ecosistema_ia.main import cargar_agentes_dinamicamente
from ecosistema_ia.agentes.tipos.testing.dummy_agents import DummyA, DummyB


def test_multiple_classes_loaded():
    agentes = cargar_agentes_dinamicamente()
    nombres = [type(a).__name__ for a in agentes]
    assert DummyA.__name__ in nombres
    assert DummyB.__name__ in nombres


def test_sequential_unique_ids():
    agentes = cargar_agentes_dinamicamente()
    ids = [a.identificador for a in agentes]
    assert len(ids) == len(set(ids))
    numeros = sorted(int(re.search(r"-(\d{3})$", i).group(1)) for i in ids)
    assert numeros == list(range(1, len(ids) + 1))


def test_base_classes_not_loaded():
    agentes = cargar_agentes_dinamicamente()
    nombres = [type(a).__name__ for a in agentes]
    assert "HerbivoroBase" not in nombres
    assert "CarnivoroBase" not in nombres
    assert "SublimeBase" not in nombres
    # topologia requires extra args; ensure no instantiation error occurs
    assert "Topologia" not in nombres

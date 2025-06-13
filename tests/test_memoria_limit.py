import ecosistema_ia.agentes.tipos.testing.dummy_agents as dummy


def test_memoria_limit_respected():
    agente = dummy.DummyA("DM-001", 0, 0, 0)
    agente.memoria_max = 5
    for i in range(10):
        agente.log_memoria(entrada=i, resultado=i * 2)
        agente.incrementar_edad()
    assert len(agente.memoria) <= agente.memoria_max

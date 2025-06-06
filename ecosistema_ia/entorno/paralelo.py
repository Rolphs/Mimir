from concurrent.futures import ProcessPoolExecutor
from typing import List


def _actuar_agente(agente, territorio, agentes):
    """Ejecuta la acción de un agente en un proceso independiente."""
    try:
        agente.actuar(territorio, otros_agentes=agentes)
    except Exception as e:
        print(f"⚠️ Error en {agente.identificador}: {e}")
    return agente


def run_parallel(agentes: List, territorio, max_workers: int | None = None) -> List:
    """Lanza la fase de actuación de los agentes usando múltiples procesos.

    :param agentes: lista de agentes a ejecutar.
    :param territorio: instancia compartida del territorio.
    :param max_workers: opcional, número máximo de procesos.
    :return: lista de agentes actualizados tras actuar.
    """
    tareas = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for agente in agentes:
            tareas.append(executor.submit(_actuar_agente, agente, territorio, agentes))
        resultados = []
        for futuro in tareas:
            try:
                resultados.append(futuro.result())
            except Exception as e:
                print(f"⚠️ Error en ejecución paralela: {e}")
    return resultados

__all__ = ["run_parallel"]

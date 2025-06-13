import random
from typing import List, Dict


class MetaRegulador:
    """Supervisa las métricas del ecosistema e introduce perturbaciones
    cuando detecta estabilidad prolongada."""

    def __init__(self, ventana: int = 3, variacion_min: float = 0.01):
        self.ventana = ventana
        self.variacion_min = variacion_min
        self.historial: List[Dict[str, float]] = []
        self.acciones = 0

    def evaluar(self, territorio, agentes) -> Dict[str, float]:
        """Evalúa las métricas actuales y aplica perturbaciones si es necesario."""
        metricas = territorio.calcular_metricas(agentes)
        self.historial.append(metricas)
        if len(self.historial) > self.ventana:
            self.historial.pop(0)

        if len(self.historial) == self.ventana and self._es_estable():
            self._perturbar(territorio, agentes)
        return metricas

    def _es_estable(self) -> bool:
        densidades = [m["densidad"] for m in self.historial]
        diversidades = [m["diversidad"] for m in self.historial]
        tensiones = [m["tension"] for m in self.historial]
        return (
            max(densidades) - min(densidades) < self.variacion_min
            and max(diversidades) - min(diversidades) < self.variacion_min
            and max(tensiones) - min(tensiones) < self.variacion_min
        )

    def _perturbar(self, territorio, agentes) -> None:
        """Introduce pequeñas variaciones para romper la estabilidad."""
        self.acciones += 1
        for agente in agentes:
            agente.mover(
                dx=random.choice([-1, 1]),
                dy=random.choice([-1, 1]),
                dz=random.choice([-1, 0, 1]),
                territorio=territorio,
            )
            agente.broadcast_mensaje(territorio, "perturbacion", tipo="conflicto")
        print("\U0001F32A\ufe0f MetaRegulador introdujo perturbaciones")


__all__ = ["MetaRegulador"]

# omnivoro_base.py

"""Base class for omnivorous agents capable of consuming data and interacting with others."""

from ecosistema_ia.agentes.agente_base import AgenteBase


class OmnivoroBase(AgenteBase):
    """Minimal base for omnivore agents."""

    def __init__(self, identificador, x, y, z, funcion="omnivoro"):
        super().__init__(identificador, x, y, z, funcion=funcion)

    def consumir_dato(self, territorio):
        """Consume data from the current position and log the reward."""
        datos = territorio.get_csv(self.z)
        if not datos:
            self.alimentacion = None
            return 0

        self.x = max(0, min(self.x, len(datos) - 1))
        fila = datos[self.x]
        if not fila:
            self.alimentacion = None
            return 0

        self.y = max(0, min(self.y, len(fila) - 1))
        self.alimentacion = fila[self.y]
        recompensa = len(str(self.alimentacion)) if self.alimentacion else 0
        self.recompensa_total += recompensa
        self.log_memoria(
            entrada=self.alimentacion,
            resultado={"recompensa": recompensa},
            exitoso=recompensa > 0,
        )
        return recompensa

    def buscar_vecinos(self, agentes):
        """Return nearby agents within a 2 cell radius on the same Z layer."""
        return [
            a for a in agentes
            if a.identificador != self.identificador
            and a.z == self.z
            and abs(a.x - self.x) <= 2
            and abs(a.y - self.y) <= 2
        ]


__all__ = ["OmnivoroBase"]

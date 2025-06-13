# omni_colector.py

"""Omnivorous agent that consumes data and absorbs the memory of nearby agents."""

from ecosistema_ia.agentes.tipos.omnivoros.omnivoro_base import OmnivoroBase


class OmniColector(OmnivoroBase):
    """Agent that harvests information from the territory and neighbours."""

    def __init__(self, identificador, x, y, z):
        super().__init__(identificador, x, y, z, funcion="omni_colector")

    def absorber_memorias(self, vecinos):
        """Take memory entries from neighbouring agents."""
        for vecino in vecinos:
            if getattr(vecino, "memoria", []):
                self.memoria.extend(vecino.memoria)
                vecino.memoria.clear()
                self.log_memoria(
                    entrada=f"memoria de {vecino.identificador}",
                    resultado=f"absorvidas {len(self.memoria)} entradas",
                    exitoso=True,
                )
                print(f"🔄 {self.identificador} absorbió la memoria de {vecino.identificador}")

    def actuar(self, territorio, otros_agentes=None):
        self.incrementar_edad()
        self.consumir_dato(territorio)
        vecinos = self.buscar_vecinos(otros_agentes or [])
        self.absorber_memorias(vecinos)


__all__ = ["OmniColector"]

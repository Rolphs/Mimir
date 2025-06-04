# herbivoro.py

import random
from ecosistema_ia.agentes.tipos.herbivoros.herbivoro_base import HerbivoroBase

class Herbivoro(HerbivoroBase):
    """Herbívoro genérico que se desplaza aleatoriamente y recoge recompensa
    basada en la longitud del dato que consume."""

    def __init__(self, identificador, x, y, z):
        super().__init__(identificador, x, y, z, funcion="herbivoro")

    def actuar(self, territorio, otros_agentes=None):
        self.incrementar_edad()
        self.recibir_mensajes(territorio)
        datos_csv = territorio.get_csv(self.z)
        if datos_csv:
            self.x = max(0, min(self.x + random.choice([-1, 0, 1]), len(datos_csv) - 1))
            fila = datos_csv[self.x]
            if fila:
                self.y = max(0, min(self.y + random.choice([-1, 0, 1]), len(fila) - 1))
                self.alimentacion = fila[self.y]
            else:
                self.alimentacion = None
        else:
            self.alimentacion = None
        recompensa = len(str(self.alimentacion)) if self.alimentacion else 0
        self.recompensa_total += recompensa
        self.log_memoria(
            entrada=self.alimentacion,
            resultado={"recompensa": recompensa},
            exitoso=recompensa > 0,
        )

__all__ = ["Herbivoro"]

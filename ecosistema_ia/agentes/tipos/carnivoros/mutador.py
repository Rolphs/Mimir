# mutador.py

import random
from ecosistema_ia.agentes.tipos.carnivoros.carnivoro_base import CarnivoroBase
from ecosistema_ia.agentes.tipos.herbivoros.herbivoro_base import HerbivoroBase


class Mutador(CarnivoroBase):
    """Carnívoro que altera la memoria de herbívoros cercanos."""

    def __init__(self, identificador, x, y, z, max_mutaciones=3):
        super().__init__(identificador, x, y, z, funcion="mutador")
        self.mutaciones_exitosas = 0
        self.max_mutaciones = max_mutaciones

    def evaluar_objetivo(self, agente):
        return (
            isinstance(agente, HerbivoroBase)
            and agente.identificador != self.identificador
            and agente.z == self.z
            and abs(agente.x - self.x) <= 1
            and abs(agente.y - self.y) <= 1
        )

    def actuar(self, territorio, otros_agentes=None):
        self.incrementar_edad()
        agentes = otros_agentes or []
        objetivos = [a for a in agentes if self.evaluar_objetivo(a)]
        for objetivo in objetivos:
            self.interactuar(objetivo, territorio)

    def interactuar(self, objetivo, territorio):
        if not objetivo.memoria:
            self.log_memoria(
                entrada=f"{objetivo.identificador} sin memoria",
                resultado="Sin cambios",
                exitoso=False,
            )
            return

        ultimo = objetivo.memoria[-1]
        dato = str(ultimo.get("resultado", ultimo.get("entrada", "")))
        mutado = "".join(random.choice((c.upper(), c.lower())) for c in dato)
        objetivo.memoria[-1]["resultado"] = mutado
        objetivo.log_memoria(
            entrada={"mutado_por": self.identificador},
            resultado=mutado,
            exitoso=True,
        )
        self.log_memoria(
            entrada={"objetivo": objetivo.identificador, "dato_original": dato},
            resultado="mutacion",
            exitoso=True,
        )
        self.mutaciones_exitosas += 1
        print(f"🧬 {self.identificador} mutó a {objetivo.identificador} → {mutado}")

    def puede_reproducirse(self):
        return self.mutaciones_exitosas >= self.max_mutaciones

    def reproducirse(self, nuevo_id):
        nuevo_x = self.x + random.choice([-1, 0, 1])
        nuevo_y = self.y + random.choice([-1, 0, 1])
        nuevo = Mutador(nuevo_id, nuevo_x, nuevo_y, self.z, self.max_mutaciones)
        print(f"🧬 {self.identificador} creó a {nuevo.identificador} (nuevo mutador)")
        return nuevo


__all__ = ["Mutador"]

# alquimista.py

import random
from ecosistema_ia.agentes.tipos.carnivoros.carnivoro_base import CarnivoroBase

class Alquimista(CarnivoroBase):
    def __init__(self, identificador, x, y, z):
        super().__init__(identificador, x, y, z, funcion="alquimista")
        self.mutaciones_realizadas = 0
        self.max_mutaciones = 5

    def evaluar_objetivo(self, agente):
        return (
            agente.funcion != "sublime" and
            agente.identificador != self.identificador and
            agente.z == self.z and
            abs(agente.x - self.x) <= 1 and
            abs(agente.y - self.y) <= 1
        )

    def interactuar(self, objetivo, territorio):
        if not objetivo.memoria:
            self.log_memoria("Sin memoria en objetivo", "No se pudo alterar", exitoso=False)
            return

        entrada = str(objetivo.memoria[-1])
        tipo = "mutacion" if random.random() < 0.5 else "reparacion"
        resultado = (
            self.mutacion_simbolica(entrada)
            if tipo == "mutacion"
            else self.reparacion_basica(entrada)
        )

        objetivo.log_memoria(entrada, resultado, exitoso=True)
        objetivo.memoria.append({
            "ciclo": self.edad,
            "tipo_alquimia": tipo,
            "resultado": resultado
        })
        self.mutaciones_realizadas += 1

        self.log_memoria(
            entrada={"objetivo": objetivo.identificador, "tipo": tipo},
            resultado=resultado,
            exitoso=True
        )
        print(f"🧪 {self.identificador} alteró a {objetivo.identificador} → {resultado[:30]}...")

    def mutacion_simbolica(self, texto):
        simbolos = ["@", "#", "$", "%", "&", "*"]
        return "".join(c if random.random() > 0.2 else random.choice(simbolos) for c in texto)

    def reparacion_basica(self, texto):
        return texto.replace("None", "").replace("null", "").replace("N/A", "").strip()

    def puede_reproducirse(self):
        return self.mutaciones_realizadas >= self.max_mutaciones

    def reproducirse(self, nuevo_id):
        nuevo_x = self.x + random.choice([-1, 0, 1])
        nuevo_y = self.y + random.choice([-1, 0, 1])
        nuevo_agente = Alquimista(nuevo_id, nuevo_x, nuevo_y, self.z)
        print(f"🧬 {self.identificador} creó a {nuevo_agente.identificador} (nuevo alquimista)")
        return nuevo_agente

__all__ = ["Alquimista"]

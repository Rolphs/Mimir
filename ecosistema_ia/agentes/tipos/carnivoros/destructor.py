# destructor.py

import random
from agentes.tipos.carnivoros.carnivoro_base import CarnivoroBase

class Destructor(CarnivoroBase):
    def __init__(self, identificador="D-001", x=0, y=0, z=0):
        super().__init__(identificador, x, y, z, funcion="destructor")

    def evaluar_objetivo(self, agente):
        return hasattr(agente, "calificacion") and agente.calificacion == "roja"

    def interactuar(self, objetivo, territorio):
        if hasattr(objetivo, "memoria"):
            for entrada in objetivo.memoria:
                if isinstance(entrada, dict) and "dato" in entrada:
                    dato = entrada["dato"]
                    if dato:
                        try:
                            territorio.dispersar_dato(dato, objetivo.x, objetivo.y, objetivo.z)
                        except Exception as e:
                            print(f"⚠️ Error al dispersar dato de {objetivo.identificador}: {e}")

        self.log_memoria(
            entrada=f"Agente {objetivo.identificador} con calificación roja",
            resultado="Dispersado",
            exitoso=True
        )
        print(f"💀 {self.identificador} dispersa al agente {objetivo.identificador} por calificación roja.")

    def actuar(self, territorio, otros_agentes=None, ciclo=0):
        self.incrementar_edad()
        agentes = otros_agentes or []
        sobrevivientes = []
        dispersados = []

        for agente in agentes:
            if self.evaluar_objetivo(agente):
                self.interactuar(agente, territorio)
                dispersados.append(agente)
            else:
                sobrevivientes.append(agente)

        return sobrevivientes

    def puede_reproducirse(self):
        return False

    def reproducirse(self, nuevo_id):
        raise NotImplementedError("El Destructor no puede reproducirse.")

__all__ = ["Destructor"]
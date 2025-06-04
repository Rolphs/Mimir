"""Agent that evaluates other agents' performance."""

from ecosistema_ia.agentes.tipos.sublimes.sublime_base import SublimeBase


class Calificador(SublimeBase):
    def __init__(self, identificador="CAL-001", x=0, y=0, z=0, ciclos_observacion=3):
        super().__init__(identificador, x, y, z, funcion="calificador")
        self.ciclos_observacion = ciclos_observacion
        self.observaciones = {}  # {id_agente: [excreciones]}

    def observar(self, territorio, agentes, ciclo):
        for agente in agentes:
            if agente.identificador not in self.observaciones:
                self.observaciones[agente.identificador] = []

            self.observaciones[agente.identificador].append(agente.excrecion)

            # Mantener solo los últimos N ciclos
            self.observaciones[agente.identificador] = self.observaciones[agente.identificador][-self.ciclos_observacion:]

            # Evaluar desempeño si hay suficientes datos
            if len(self.observaciones[agente.identificador]) == self.ciclos_observacion:
                excreciones = self.observaciones[agente.identificador]
                if any(e for e in excreciones if e is not None and str(e).strip()):
                    agente.calificacion = "verde"
                else:
                    agente.calificacion = "roja"

                print(f"🏁 {self.identificador} calificó a {agente.identificador} como: {agente.calificacion}")

__all__ = ["Calificador"]


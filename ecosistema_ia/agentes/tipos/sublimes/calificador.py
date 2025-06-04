# calificador.py

class Calificador:
    def __init__(self, ciclos_observacion=3):
        self.observaciones = {}  # {id_agente: [excreciones]}
        self.ciclos_observacion = ciclos_observacion

    def observar(self, agentes):
        for agente in agentes:
            if agente.identificador not in self.observaciones:
                self.observaciones[agente.identificador] = []

            # Registrar excreción actual
            self.observaciones[agente.identificador].append(agente.excrecion)

            # Mantener solo los últimos N ciclos
            self.observaciones[agente.identificador] = self.observaciones[agente.identificador][-self.ciclos_observacion:]

            # Evaluar desempeño si hay suficientes ciclos
            if len(self.observaciones[agente.identificador]) == self.ciclos_observacion:
                excreciones = self.observaciones[agente.identificador]
                if any(e for e in excreciones if e is not None and str(e).strip()):
                    agente.calificacion = "verde"
                else:
                    agente.calificacion = "roja"

                print(f"🏁 {agente.identificador} calificado como: {agente.calificacion}")
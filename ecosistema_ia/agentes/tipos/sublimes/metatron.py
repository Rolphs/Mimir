# metatron.py

import csv
from datetime import datetime
from agentes.tipos.sublimes.sublime_base import SublimeBase

class Metatron(SublimeBase):
    def __init__(self, identificador="MET-001", x=0, y=0, z=0):
        super().__init__(identificador, x, y, z, funcion="metatron")
        self.reporte = []
        self.ruta_csv = "datos/metatron.csv"

        with open(self.ruta_csv, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["ciclo", "agente", "funcion", "edad", "x", "y", "z", "recompensa_total", "calificacion"])

    def observar(self, territorio, agentes, ciclo):
        with open(self.ruta_csv, mode='a', newline='') as f:
            writer = csv.writer(f)
            for agente in agentes:
                writer.writerow([
                    ciclo,
                    agente.identificador,
                    getattr(agente, "funcion", "desconocida"),
                    getattr(agente, "edad", 0),
                    getattr(agente, "x", -1),
                    getattr(agente, "y", -1),
                    getattr(agente, "z", -1),
                    getattr(agente, "recompensa_total", 0),
                    getattr(agente, "calificacion", "N/A")
                ])
        print(f"👁️ {self.identificador} registró {len(agentes)} agentes en el ciclo {ciclo}")

__all__ = ["Metatron"]
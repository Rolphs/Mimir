# metatron.py

import csv
import os
from collections import Counter
from ecosistema_ia.agentes.tipos.sublimes.sublime_base import SublimeBase
from ecosistema_ia.config import (
    CSV_METATRON_PATH,
    CSV_METATRON_HEATMAP_PATH,
    CSV_METATRON_SEMANTICS_PATH,
)

class Metatron(SublimeBase):
    def __init__(
        self,
        identificador: str = "MET-001",
        x: int = 0,
        y: int = 0,
        z: int = 0,
        ruta_csv: str = CSV_METATRON_PATH,
        ruta_heatmap: str = CSV_METATRON_HEATMAP_PATH,
        ruta_semantica: str = CSV_METATRON_SEMANTICS_PATH,
    ) -> None:
        super().__init__(identificador, x, y, z, funcion="metatron")
        self.reporte = []
        self.ruta_csv = str(ruta_csv)
        self.ruta_heatmap = str(ruta_heatmap)
        self.ruta_semantica = str(ruta_semantica)

        for ruta in [self.ruta_csv, self.ruta_heatmap, self.ruta_semantica]:
            os.makedirs(os.path.dirname(ruta), exist_ok=True)

        if not os.path.exists(self.ruta_csv):
            with open(self.ruta_csv, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "ciclo",
                    "agente",
                    "funcion",
                    "edad",
                    "x",
                    "y",
                    "z",
                    "recompensa_total",
                    "calificacion",
                ])

        if not os.path.exists(self.ruta_heatmap):
            with open(self.ruta_heatmap, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ciclo", "x", "y", "z", "conteo"])

        if not os.path.exists(self.ruta_semantica):
            with open(self.ruta_semantica, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ciclo", "token", "conteo"])

    def observar(self, territorio, agentes, ciclo):
        posicion_contador = Counter()
        semantico = Counter()

        with open(self.ruta_csv, mode="a", newline="", encoding="utf-8") as f:
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
                    getattr(agente, "calificacion", "N/A"),
                ])
                posicion_contador[(agente.x, agente.y, agente.z)] += 1
                for m in getattr(agente, "memoria", []):
                    texto = f"{m.get('entrada','')} {m.get('resultado','')}"
                    tokens = texto.lower().split()
                    semantico.update(tokens)

        with open(self.ruta_heatmap, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for (x, y, z), conteo in posicion_contador.items():
                writer.writerow([ciclo, x, y, z, conteo])

        with open(self.ruta_semantica, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for token, conteo in semantico.most_common(10):
                writer.writerow([ciclo, token, conteo])

        try:
            from ecosistema_ia.visualizacion.graficos import generar_heatmap
            generar_heatmap(self.ruta_heatmap, ciclo)
        except Exception as e:
            print(f"⚠️ Error generando heatmap: {e}")

        print(f"👁️ {self.identificador} registró {len(agentes)} agentes en el ciclo {ciclo}")

__all__ = ["Metatron"]

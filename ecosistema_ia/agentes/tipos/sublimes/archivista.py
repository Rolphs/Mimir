"""Agente sublime que registra el estado de todos los agentes en cada ciclo."""

import csv
import os
from collections import Counter, defaultdict
from ecosistema_ia.agentes.tipos.sublimes.sublime_base import SublimeBase
from ecosistema_ia.config import DATA_DIR


class Archivista(SublimeBase):
    """Observador que guarda descripciones y resume estadísticas globales."""

    def __init__(self, identificador="ARC-001", x=0, y=0, z=0,
                 ruta_csv: str | None = None) -> None:
        ruta = DATA_DIR / "archivista.csv" if ruta_csv is None else ruta_csv
        super().__init__(identificador, x, y, z, funcion="archivista")
        self.ruta_csv = str(ruta)
        os.makedirs(os.path.dirname(self.ruta_csv), exist_ok=True)
        if not os.path.exists(self.ruta_csv):
            with open(self.ruta_csv, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "ciclo",
                    "id",
                    "funcion",
                    "posicion",
                    "edad",
                    "recompensa_total",
                    "memoria_len",
                    "alianzas",
                    "calificacion",
                ])

    def observar(self, territorio, agentes, ciclo: int) -> None:
        """Registra descripciones y muestra estadísticas simples."""
        conteo_tipo = Counter()
        recompensas = defaultdict(list)
        with open(self.ruta_csv, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            for a in agentes:
                desc = a.describir()
                writer.writerow([
                    ciclo,
                    desc.get("id"),
                    desc.get("funcion"),
                    desc.get("posicion"),
                    desc.get("edad"),
                    desc.get("recompensa_total"),
                    desc.get("memoria_len"),
                    "|".join(desc.get("alianzas", [])),
                    desc.get("calificacion"),
                ])
                tipo = desc.get("funcion", "desconocido")
                conteo_tipo[tipo] += 1
                recompensas[tipo].append(desc.get("recompensa_total", 0))

        print(f"🗂️ {self.identificador} registró {len(agentes)} agentes en el ciclo {ciclo}")
        total_recomp = [r for rs in recompensas.values() for r in rs]
        if total_recomp:
            prom_global = sum(total_recomp) / len(total_recomp)
        else:
            prom_global = 0
        print(f"   Recompensa promedio global: {prom_global:.2f}")
        for tipo, cant in conteo_tipo.items():
            lista = recompensas[tipo]
            avg = sum(lista) / len(lista) if lista else 0
            print(f"   {tipo}: {cant} agentes | recompensa media: {avg:.2f}")


__all__ = ["Archivista"]

# mensajero.py

import csv
import os
from datetime import datetime
from collections import Counter
from ecosistema_ia.agentes.tipos.sublimes.sublime_base import SublimeBase

class Mensajero(SublimeBase):
    def __init__(self, identificador="MSG-001", x=0, y=0, z=0, ruta_reporte="datos/metatron_mensajes.csv", umbral_patrones: int = 3):
        super().__init__(identificador, x, y, z, funcion="mensajero")
        self.reporte_path = ruta_reporte
        os.makedirs(os.path.dirname(self.reporte_path), exist_ok=True)
        self._inicializar_archivo()
        self.historial = []
        self.umbral_patrones = umbral_patrones
        self.patrones_actuales = {}

    def _inicializar_archivo(self):
        if not os.path.exists(self.reporte_path):
            with open(self.reporte_path, mode="w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",
                    "ciclo",
                    "tipo_mensaje",
                    "posicion",
                    "dato_hash",
                    "emisor_visible"
                ])

    def observar(self, territorio, agentes, ciclo):
        buzon_mensajes = territorio.buzon_mensajes
        if not buzon_mensajes:
            return

        timestamp = datetime.utcnow().isoformat()

        with open(self.reporte_path, mode="a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for m in buzon_mensajes:
                tipo = m.get("tipo", "desconocido")
                x = m.get("x", "?")
                y = m.get("y", "?")
                z = m.get("z", "?")
                posicion = f"({x}, {y}, {z})"
                dato_hash = m.get("dato_util", "???")
                emisor = m.get("emisor", "anónimo")

                writer.writerow([
                    timestamp,
                    ciclo,
                    tipo,
                    posicion,
                    dato_hash,
                    emisor
                ])
                self.historial.append({
                    "ciclo": ciclo,
                    "emisor": emisor,
                    "pos": (x, y, z),
                    "tipo": tipo,
                    "dato": dato_hash
                })

        print(f"📨 {self.identificador} registró {len(buzon_mensajes)} mensajes en el ciclo {ciclo}.")
        self.detectar_patrones(ciclo, territorio)

    def detectar_patrones(self, ciclo_actual, territorio):
        ultimos = [m for m in self.historial if ciclo_actual - m["ciclo"] <= 5]

        emisores = Counter(m["emisor"] for m in ultimos)
        zonas = Counter(m["pos"] for m in ultimos)
        tipos = Counter(m["tipo"] for m in ultimos)

        patrones = {}
        if emisores:
            top_emisor = emisores.most_common(1)[0]
            patrones["emisor"] = top_emisor[0]
            print(f"👁️ {self.identificador} detecta emisor dominante: {top_emisor[0]} ({top_emisor[1]} mensajes)")

        if zonas:
            zona_caliente = zonas.most_common(1)[0]
            patrones["zona"] = zona_caliente[0]
            print(f"🔥 {self.identificador} detecta zona activa: {zona_caliente[0]} ({zona_caliente[1]} mensajes)")

        if tipos:
            tipo_dominante = tipos.most_common(1)[0]
            patrones["tipo"] = tipo_dominante[0]
            print(f"📡 {self.identificador} detecta mensaje dominante: tipo '{tipo_dominante[0]}' ({tipo_dominante[1]} ocurrencias)")

        for k, val in patrones.items():
            actual = self.patrones_actuales.get(k)
            if actual and actual["valor"] == val:
                actual["duracion"] += 1
            else:
                actual = {"valor": val, "duracion": 1}
            self.patrones_actuales[k] = actual
            if actual["duracion"] > self.umbral_patrones:
                territorio.desmontar_patron(k, val)
                self.patrones_actuales[k] = {"valor": None, "duracion": 0}

__all__ = ["Mensajero"]

import csv
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from sklearn.linear_model import LinearRegression
from ..config import DATA_DIR, DATASETS_DIR


class Territorio:
    def __init__(
        self,
        ruta_base: Path = DATASETS_DIR,
        ruta_csv_intocable: Path = DATA_DIR / "territorio.csv",
        ruta_eliminaciones: Path = DATA_DIR / "logs" / "eliminaciones.csv",
    ) -> None:
        self.ruta_base = Path(ruta_base)
        self.ruta_csv_intocable = Path(ruta_csv_intocable)
        self.ruta_eliminaciones = Path(ruta_eliminaciones)
        # En lugar de cargar todas las filas en memoria, sólo mantenemos las
        # rutas de cada CSV para permitir que la carpeta contenga miles o
        # incluso millones de archivos sin agotar recursos.
        self.csvs = self.cargar_datasets()
        self.buzon_mensajes = []  # 📬 Espacio compartido para comunicación entre agentes
        self.historial_estados = []
        self.modelo = None
        print("🧭 Territorio inicializado")

    def cargar_datasets(self) -> List[Path]:
        """Devuelve las rutas de los archivos CSV ordenadas por fecha y nombre."""
        archivos = []
        if not self.ruta_base.exists():
            print(f"⚠️ Ruta no encontrada: {self.ruta_base}")
            return archivos

        archivos_csv = []
        for archivo in self.ruta_base.iterdir():
            if archivo.suffix == ".csv":
                try:
                    timestamp = archivo.stat().st_ctime
                except OSError:
                    timestamp = 0
                archivos_csv.append((timestamp, archivo))

        archivos_csv.sort(key=lambda x: (x[0], x[1].name))
        for _, archivo in archivos_csv:
            archivos.append(archivo)

        return archivos

    def get_csv(self, z: int) -> List[List[str]]:
        """Carga y devuelve el CSV de la dimensión solicitada."""
        if 0 <= z < len(self.csvs):
            ruta = self.csvs[z]
            try:
                with ruta.open(newline='', encoding='utf-8') as f:
                    return [fila for fila in csv.reader(f)]
            except Exception as e:
                print(f"⚠️ Error al leer {ruta}: {e}")
        return []

    def renderizar(self):
        print("🌍 Territorio renderizado")
        estado = {f"z{z}": ruta.name for z, ruta in enumerate(self.csvs)}
        print(f"CSV disponibles: {estado}")

    def renderizar_agentes_ascii(self, agentes):
        print("🧬 Mapa de Agentes:")
        mapa = {}
        for a in agentes:
            key = (a.x, a.y, a.z)
            mapa.setdefault(key, []).append(a.identificador)
        for key, ids in sorted(mapa.items()):
            print(f"  📍 {key} → {ids}")

    def eliminar_agentes_ineficientes(self, agentes, umbral=1, ciclo=0) -> List:
        vivos = [a for a in agentes if a.recompensa_total >= umbral]
        muertos = [a for a in agentes if a.recompensa_total < umbral]
        if muertos:
            print(f"💀 Eliminados {len(muertos)} agentes por baja eficiencia.")
            self.registrar_eliminaciones_csv(muertos, ciclo)
        return vivos

    def registrar_eliminaciones_csv(self, eliminados, ciclo: int):
        self.ruta_eliminaciones.parent.mkdir(parents=True, exist_ok=True)
        nuevo = not self.ruta_eliminaciones.exists()
        with self.ruta_eliminaciones.open("a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if nuevo:
                writer.writerow(["ciclo", "timestamp", "id", "recompensa_total", "edad", "posicion", "alianzas"])
            for a in eliminados:
                writer.writerow([
                    ciclo,
                    datetime.utcnow().isoformat(),
                    a.identificador,
                    a.recompensa_total,
                    a.edad,
                    f"({a.x},{a.y},{a.z})",
                    "|".join(sorted(a.alianzas))
                ])

    def registrar_estado_csv(self, ciclo: int, total_agentes: int):
        estado = {
            "ciclo": ciclo,
            "timestamp": datetime.utcnow().isoformat(),
            "agentes": total_agentes
        }
        self.historial_estados.append(estado)
        self.ruta_csv_intocable.parent.mkdir(parents=True, exist_ok=True)
        nuevo = not self.ruta_csv_intocable.exists()
        with self.ruta_csv_intocable.open("a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if nuevo:
                writer.writerow(["ciclo", "timestamp", "agentes"])
            writer.writerow([estado["ciclo"], estado["timestamp"], estado["agentes"]])

    def entrenar_modelo_territorio(self):
        if len(self.historial_estados) < 5:
            print("📉 No hay suficientes datos para entrenar el modelo de regulación.")
            return
        X = [[e["ciclo"]] for e in self.historial_estados]
        y = [e["agentes"] for e in self.historial_estados]
        self.modelo = LinearRegression().fit(X, y)

    def get_prediccion_poblacion(self, ciclo: int) -> int:
        if self.modelo:
            return int(self.modelo.predict([[ciclo]])[0])
        return -1

    def get_estado_json(self) -> Dict:
        if not self.historial_estados:
            return {}
        ultimo = self.historial_estados[-1]
        return {
            "ciclo": ultimo["ciclo"],
            "timestamp": ultimo["timestamp"],
            "agentes": ultimo["agentes"],
            "prediccion_siguiente": self.get_prediccion_poblacion(ultimo["ciclo"] + 1)
        }

    def regular(self, agentes, ciclo=0):
        print(f"📊 Regulando ecosistema | Ciclo {ciclo} | Agentes: {len(agentes)}")
        self.registrar_estado_csv(ciclo, len(agentes))
        self.entrenar_modelo_territorio()
        pred = self.get_prediccion_poblacion(ciclo + 1)
        if pred != -1 and len(agentes) > pred * 1.2:
            print(f"⚠️ Sobrepoblación detectada. Limpiando con umbral más alto.")
            agentes = self.eliminar_agentes_ineficientes(agentes, umbral=5, ciclo=ciclo)
        else:
            agentes = self.eliminar_agentes_ineficientes(agentes, umbral=1, ciclo=ciclo)
        self.renderizar_agentes_ascii(agentes)
        return agentes

    def dispersar_dato(self, dato, x, y, z):
        if 0 <= z < len(self.csvs):
            ruta = self.csvs[z]
            try:
                with ruta.open(newline='', encoding='utf-8') as f:
                    datos_csv = [fila for fila in csv.reader(f)]
                while len(datos_csv) <= x:
                    datos_csv.append([])
                fila = datos_csv[x]
                while len(fila) <= y:
                    fila.append("")
                if not datos_csv[x][y]:
                    datos_csv[x][y] = str(dato)
                else:
                    datos_csv[x][y] += f" | {str(dato)}"
                with ruta.open('w', newline='', encoding='utf-8') as f:
                    csv.writer(f).writerows(datos_csv)
                print(f"🌀 Dato dispersado en ({x},{y},{z}): {dato}")
            except Exception as e:
                print(f"⚠️ Error al dispersar dato en ({x},{y},{z}): {e}")

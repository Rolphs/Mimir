# herbivoro_base.py

import random
import hashlib
from ecosistema_ia.agentes.agente_base import AgenteBase
from collections import defaultdict
from sklearn.linear_model import LogisticRegression

class HerbivoroBase(AgenteBase):
    vocabulario_global = defaultdict(list)

    def __init__(self, identificador, x, y, z, funcion="herbivoro"):
        super().__init__(identificador, x, y, z, funcion=funcion)
        self.prioridad = 0
        self.modelo_ml = LogisticRegression()
        self.entrenado = False
        self.X_train = []
        self.y_train = []
        self.historial_beneficio_mensajes = set()

    def recibir_mensajes(self, territorio):
        mensajes_relevantes = [
            m for m in territorio.buzon_mensajes
            if m["z"] == self.z and abs(m["x"] - self.x) <= 2 and abs(m["y"] - self.y) <= 2
        ]
        if mensajes_relevantes:
            mensaje_objetivo = random.choice(mensajes_relevantes)
            self.x = mensaje_objetivo["x"]
            self.y = mensaje_objetivo["y"]
            print(f"📡 {self.identificador} recibió mensaje y se movió a ({self.x}, {self.y}, {self.z})")
            self.recibir_mensaje(mensaje_objetivo)
            self.historial_beneficio_mensajes.add(mensaje_objetivo["emisor"])

    def emitir_mensaje(self, territorio, mensaje, recompensa, tipo_dato):
        codificado = hashlib.sha1(str(mensaje).encode()).hexdigest()[:6]
        HerbivoroBase.vocabulario_global[codificado].append((tipo_dato, recompensa))
        territorio.buzon_mensajes.append({
            "emisor": self.identificador,
            "funcion": self.funcion,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "dato_util": codificado,
            "original": mensaje,
            "recompensa": recompensa,
            "tipo_dato": tipo_dato,
            "ciclo": self.edad,
            "tipo": "descubrimiento"
        })

    def entrenar_modelo(self):
        if len(self.X_train) >= 5:
            clases = set(self.y_train)
            if len(clases) < 2:
                opuesta = 0 if list(clases)[0] == 1 else 1
                self.X_train.append([0, 0, 0])
                self.y_train.append(opuesta)
                print(f"🧪 {self.identificador} insertó muestra sintética para estabilizar el entrenamiento.")
            self.modelo_ml.fit(self.X_train, self.y_train)
            self.entrenado = True

    def reforzar_modelo(self, x, y, dato, positivo=True):
        score = len(str(dato)) if dato else 0
        self.X_train.append([x, y, score])
        self.y_train.append(1 if positivo else 0)
        self.entrenar_modelo()

    def buscar_mejor_celda(self, datos_csv, evitar=None):
        evitar = evitar or []
        mejor_score = -1
        mejor_pos = (self.x, self.y)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = self.x + dx, self.y + dy
                if (nx, ny, self.z) in evitar:
                    continue
                try:
                    valor = datos_csv[nx][ny]
                    score = len(str(valor)) if valor else 0
                    if self.entrenado:
                        score *= self.modelo_ml.predict_proba([[nx, ny, score]])[0][1]
                    if score > mejor_score:
                        mejor_score = score
                        mejor_pos = (nx, ny)
                except (IndexError, TypeError):
                    continue
        return mejor_pos

    def obtener_contexto_ambiental(self, datos_csv, aliados):
        celdas_utiles = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = self.x + dx, self.y + dy
                try:
                    if datos_csv[nx][ny] and len(str(datos_csv[nx][ny])) > 5:
                        celdas_utiles += 1
                except (IndexError, TypeError):
                    continue
        aliados_cercanos = sum(
            1 for a in aliados if abs(a.x - self.x) <= 2 and abs(a.y - self.y) <= 2 and a.z == self.z
        )
        return {"celdas_utiles": celdas_utiles, "alianzas_cercanas": aliados_cercanos}

__all__ = ["HerbivoroBase"]

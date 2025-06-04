# divisor_reproductor.py

import random
import hashlib
from datetime import datetime
from sklearn.linear_model import LogisticRegression
from agentes.tipos.carnivoros.carnivoro_base import CarnivoroBase
from agentes.tipos.herbivoros.herbivoro import Herbivoro

class DivisorReproductor(CarnivoroBase):
    historial_combinaciones = []

    def __init__(self, identificador=None, x=0, y=0, z=0):
        super().__init__(identificador or f"DR-{random.randint(1000, 9999)}", x, y, z, funcion="divisor_reproductor")
        self.memoria_acciones = []
        self.modelo_ml = LogisticRegression()
        self.X_train = []
        self.y_train = []
        self.entrenado = False
        self.ciclos_sin_reproducir = 0

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

    def reforzar_modelo(self, edad, prioridad, exito=True):
        etiqueta = 1 if exito else 0
        self.X_train.append([edad, prioridad, random.randint(1, 100)])
        self.y_train.append(etiqueta)
        self.entrenar_modelo()

    def buscar_pareja(self, agentes):
        candidatos = [a for a in agentes if hasattr(a, "memoria") and a.memoria and a.funcion == "herbivoro"]
        if len(candidatos) < 2:
            return None, None
        parejas = [(a1, a2) for i, a1 in enumerate(candidatos) for a2 in candidatos[i+1:]]
        return random.choice(parejas) if parejas else (None, None)

    def evaluar_objetivo(self, agente):
        return agente.funcion == "herbivoro" and bool(agente.memoria)

    def interactuar(self, objetivo, territorio):
        # No se usa en este agente: usa parejas, no un solo objetivo
        pass

    def recombinar_codigo(self, agente_a, agente_b):
        memoria_a = agente_a.memoria[-1] if agente_a.memoria else {}
        memoria_b = agente_b.memoria[-1] if agente_b.memoria else {}

        nuevo_x = (agente_a.x + agente_b.x) // 2
        nuevo_y = (agente_a.y + agente_b.y) // 2
        nuevo_z = agente_a.z
        nuevo_id = f"H-{hashlib.sha1(f'{agente_a.identificador}{agente_b.identificador}'.encode()).hexdigest()[:6]}"

        nuevo_agente = Herbivoro(nuevo_id, nuevo_x, nuevo_y, nuevo_z)
        nuevo_agente.memoria = [memoria_a, memoria_b]
        nuevo_agente.alianzas = agente_a.alianzas.union(agente_b.alianzas)
        nuevo_agente.prioridad = (getattr(agente_a, "prioridad", 0) + getattr(agente_b, "prioridad", 0)) // 2
        nuevo_agente.recompensa_total = 0

        self.memoria_acciones.append({
            "timestamp": datetime.utcnow().isoformat(),
            "nuevo_id": nuevo_id,
            "padres": (agente_a.identificador, agente_b.identificador),
            "posicion": (nuevo_x, nuevo_y, nuevo_z),
            "prioridades": (getattr(agente_a, "prioridad", 0), getattr(agente_b, "prioridad", 0)),
            "memoria_a": memoria_a,
            "memoria_b": memoria_b
        })

        DivisorReproductor.historial_combinaciones.append((agente_a.identificador, agente_b.identificador, nuevo_id))
        print(f"🧬 {self.identificador} creó nuevo agente recombinado: {nuevo_id} desde {agente_a.identificador} + {agente_b.identificador}")
        return nuevo_agente

    def evaluar_estado(self, agentes):
        herbivoros = [a for a in agentes if a.funcion == "herbivoro"]
        if len(herbivoros) < 4:
            return False
        diversidad = len(set(a.identificador.split("-")[0] for a in herbivoros))
        return diversidad > 1

    def actuar(self, territorio, otros_agentes=None):
        self.incrementar_edad()
        self.ciclos_sin_reproducir += 1
        agentes = otros_agentes or []

        if not self.evaluar_estado(agentes):
            print(f"🧬 {self.identificador} decide no actuar: baja diversidad o pocos agentes.")
            return []

        a1, a2 = self.buscar_pareja(agentes)
        if not a1 or not a2:
            print(f"⚠️ {self.identificador} no encontró suficientes agentes para recombinar.")
            return []

        if self.entrenado:
            pred = self.modelo_ml.predict_proba([
                [max(a1.edad, a2.edad), max(getattr(a1, "prioridad", 0), getattr(a2, "prioridad", 0)), random.randint(1, 100)]
            ])[0][1]
            if pred < 0.5:
                print(f"🔬 {self.identificador} evitó recombinación con baja predicción de éxito ({pred:.2f})")
                return []

        nuevo = self.recombinar_codigo(a1, a2)
        self.reforzar_modelo(max(a1.edad, a2.edad), max(getattr(a1, "prioridad", 0), getattr(a2, "prioridad", 0)), exito=True)
        self.ciclos_sin_reproducir = 0
        return [nuevo]

__all__ = ["DivisorReproductor"]
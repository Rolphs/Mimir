# agente_base.py

import random
from collections import deque

class AgenteBase:
    def __init__(self, identificador, x, y, z, funcion="agente"):
        self.identificador = identificador
        self.x = x
        self.y = y
        self.z = z
        self.funcion = funcion

        self.edad = 0
        self.memoria = []
        self.recompensa_total = 0
        self.alianzas = set()

        self.calificacion = None
        self.alimentacion = None
        self.excrecion = None

        self.mensajeria = deque(maxlen=10)
        self.modelo_ml = None
        self.X_train = []
        self.y_train = []
        self.entrenado = False

    def __repr__(self):
        return f"{self.funcion.capitalize()}({self.identificador} at {self.x},{self.y},{self.z})"

    @property
    def posicion(self):
        return (self.x, self.y, self.z)

    def incrementar_edad(self):
        self.edad += 1

    def puede_reproducirse(self):
        return False

    def reproducirse(self, nuevo_id):
        raise NotImplementedError("Este agente no tiene lógica de reproducción definida.")

    def actuar(self, territorio, otros_agentes=None):
        raise NotImplementedError("Este agente no tiene comportamiento definido.")

    def log_memoria(self, entrada, resultado, exitoso=False):
        self.memoria.append({
            "edad": self.edad,
            "entrada": entrada,
            "resultado": resultado,
            "exitoso": exitoso
        })

    def enviar_mensaje(self, mensaje, receptor):
        receptor.recibir_mensaje((self.identificador, mensaje))

    def recibir_mensaje(self, mensaje):
        self.mensajeria.append(mensaje)

    def describir(self):
        return {
            "id": self.identificador,
            "funcion": self.funcion,
            "posicion": self.posicion,
            "edad": self.edad,
            "recompensa_total": self.recompensa_total,
            "memoria_len": len(self.memoria),
            "alianzas": list(self.alianzas),
            "calificacion": self.calificacion
        }

    # ML
    def inicializar_modelo(self, modelo):
        self.modelo_ml = modelo

    def entrenar_modelo(self):
        if self.modelo_ml and len(self.X_train) >= 5:
            clases = set(self.y_train)
            if len(clases) < 2:
                opuesta = 0 if list(clases)[0] == 1 else 1
                self.X_train.append([0, 0, 0])
                self.y_train.append(opuesta)
                print(f"🧠 {self.identificador} insertó muestra sintética para entrenar.")
            self.modelo_ml.fit(self.X_train, self.y_train)
            self.entrenado = True

    def reforzar_modelo(self, features, etiqueta):
        self.X_train.append(features)
        self.y_train.append(1 if etiqueta else 0)
        self.entrenar_modelo()
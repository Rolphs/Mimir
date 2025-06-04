# topologia.py

import random
from ecosistema_ia.agentes.tipos.herbivoros.herbivoro_base import HerbivoroBase
from sklearn.linear_model import LogisticRegression

class Topologia(HerbivoroBase):
    def __init__(self, identificador, x, y, z, total_dimensiones):
        super().__init__(identificador, x, y, z, funcion="topologia")
        self.total_dimensiones = total_dimensiones
        self.modelo = LogisticRegression()
        self.entrenado = False
        self.X_train = []
        self.y_train = []

    def explorar_z(self, territorio):
        resultados = []
        for zi in range(self.total_dimensiones):
            datos = territorio.get_csv(zi)
            score = self.evaluar_dataset(datos)
            resultados.append((zi, score))
        resultados.sort(key=lambda x: x[1], reverse=True)
        mejor_z, mejor_score = resultados[0] if resultados else (self.z, 0)
        return mejor_z, mejor_score

    def evaluar_dataset(self, datos_csv):
        if not datos_csv:
            return 0
        non_empty = sum(1 for fila in datos_csv for celda in fila if celda and str(celda).strip())
        largo_total = sum(len(str(celda)) for fila in datos_csv for celda in fila if celda and str(celda).strip())
        promedio = largo_total / non_empty if non_empty else 0
        return promedio

    def entrenar(self):
        if len(self.X_train) >= 5 and len(set(self.y_train)) > 1:
            self.modelo.fit(self.X_train, self.y_train)
            self.entrenado = True
            print(f"🤖 {self.identificador} ha entrenado su modelo de exploración Z.")

    def reforzar(self, z, promedio, bueno=True):
        self.X_train.append([z, promedio])
        self.y_train.append(1 if bueno else 0)
        self.entrenar()

    def actuar(self, territorio, otros_agentes=None):
        self.incrementar_edad()
        mejor_z, score = self.explorar_z(territorio)

        if mejor_z != self.z:
            self.reforzar(mejor_z, score, bueno=True)
            self.log_memoria(
                entrada={"z_actual": self.z, "candidatos": self.total_dimensiones},
                resultado={"nuevo_z": mejor_z, "score": score},
                exitoso=True
            )
            print(f"🧭 {self.identificador} cruzó de Z{self.z} a Z{mejor_z} (score={score:.2f})")
            self.z = mejor_z
        else:
            self.reforzar(self.z, score, bueno=False)
            self.log_memoria(
                entrada={"z_actual": self.z, "candidatos": self.total_dimensiones},
                resultado={"nuevo_z": self.z, "score": score},
                exitoso=False
            )
            print(f"🔍 {self.identificador} permanece en Z{self.z} (score={score:.2f})")

        # Mensaje automático para otros agentes
        mensaje = f"Mejor zona Z detectada: Z{mejor_z} con score {score:.2f}"
        if otros_agentes:
            for agente in otros_agentes:
                self.emitir_mensaje(territorio, mensaje, 0, "z_topologia")

__all__ = ["Topologia"]

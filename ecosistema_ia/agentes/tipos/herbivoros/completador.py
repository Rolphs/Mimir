# completador.py

import random
from ecosistema_ia.agentes.tipos.herbivoros.herbivoro_base import HerbivoroBase

class Completador(HerbivoroBase):
    def __init__(self, identificador, x, y, z):
        super().__init__(identificador, x, y, z, funcion="completador")
        self.acciones_realizadas = 0

    def actuar(self, territorio, otros_agentes=None):
        self.incrementar_edad()
        self.recibir_mensajes(territorio)

        aliados = [a for a in (otros_agentes or []) if a.identificador in self.alianzas]
        datos_csv = territorio.get_csv(self.z)
        self.x, self.y = self.buscar_mejor_celda(datos_csv)

        try:
            celda = datos_csv[self.x][self.y]
        except (IndexError, TypeError):
            celda = None

        if not celda or str(celda).strip() == "":
            valor_predecido = self.predecir_valor(datos_csv)
            if valor_predecido:
                datos_csv[self.x][self.y] = valor_predecido
                self.acciones_realizadas += 1
                self.recompensa_total += 1
                self.emitir_mensaje(territorio, valor_predecido, 1, "completado")
                self.reforzar_modelo(self.x, self.y, valor_predecido, positivo=True)
                self.log_memoria(
                    entrada="Celda vacía detectada",
                    resultado=f"Completado con: {valor_predecido}",
                    exitoso=True
                )
                print(f"🧩 {self.identificador} completó {self.posicion} con: {valor_predecido}")
            else:
                self.reforzar_modelo(self.x, self.y, valor_predecido, positivo=False)
                self.log_memoria(
                    entrada="Celda vacía detectada",
                    resultado="Sin valor predecido disponible",
                    exitoso=False
                )
                print(f"⚠️ {self.identificador} no pudo completar {self.posicion}")
        else:
            self.reforzar_modelo(self.x, self.y, celda, positivo=False)
            self.log_memoria(
                entrada="Celda ya tenía valor",
                resultado=f"Valor existente: {celda}",
                exitoso=False
            )
            print(f"🔎 {self.identificador} encontró valor en {self.posicion}")

    def predecir_valor(self, datos_csv):
        muestras = []
        for fila in datos_csv[max(0, self.x - 2):self.x + 3]:
            for valor in fila[max(0, self.y - 2):self.y + 3]:
                if valor and str(valor).strip():
                    muestras.append(valor)
        return random.choice(muestras) if muestras else None

    def puede_reproducirse(self):
        return self.acciones_realizadas >= 3

    def reproducirse(self, nuevo_id):
        nuevo_x = max(0, self.x + random.choice([-1, 0, 1]))
        nuevo_y = max(0, self.y + random.choice([-1, 0, 1]))
        nuevo_agente = Completador(nuevo_id, nuevo_x, nuevo_y, self.z)
        nuevo_agente.memoria = self.memoria[-5:]
        nuevo_agente.alianzas = set(self.alianzas)
        print(f"🧬 {self.identificador} creó a {nuevo_agente.identificador} (nuevo completador)")
        return nuevo_agente

__all__ = ["Completador"]

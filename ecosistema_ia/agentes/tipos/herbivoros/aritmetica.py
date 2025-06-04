# aritmetica.py

import random
import math
from ecosistema_ia.agentes.tipos.herbivoros.herbivoro_base import HerbivoroBase

class Aritmetica(HerbivoroBase):
    def __init__(self, identificador, x, y, z):
        super().__init__(identificador, x, y, z, funcion="aritmetica")
        self.operacion = self.operacion_basica  # Por ahora, usa cuadrado

    def operacion_basica(self, valor):
        try:
            return float(valor) ** 2  # Ejemplo: eleva al cuadrado
        except (ValueError, TypeError):
            return None

    def actuar(self, territorio, otros_agentes=None):
        self.incrementar_edad()
        self.recibir_mensajes(territorio)

        aliados = [a for a in (otros_agentes or []) if a.identificador in self.alianzas]
        ocupadas = [(a.x, a.y, a.z) for a in aliados]
        datos_csv = territorio.get_csv(self.z)

        self.x, self.y = self.buscar_mejor_celda(datos_csv, evitar=ocupadas)

        try:
            self.alimentacion = datos_csv[self.x][self.y]
        except (IndexError, TypeError):
            self.alimentacion = None

        recompensa = 0
        self.excrecion = None

        if self.alimentacion:
            resultado = self.operacion(self.alimentacion)
            if resultado is not None:
                self.excrecion = resultado
                recompensa = len(str(resultado))
                self.recompensa_total += recompensa
                tipo_dato = type(self.alimentacion).__name__

                self.emitir_mensaje(territorio, resultado, recompensa, tipo_dato)
                self.reforzar_modelo(self.x, self.y, resultado, positivo=True)

                print(f"➕ {self.identificador} procesó {self.alimentacion} → {resultado} en {self.posicion}")
            else:
                self.reforzar_modelo(self.x, self.y, self.alimentacion, positivo=False)
                print(f"❌ {self.identificador} no pudo procesar {self.alimentacion} en {self.posicion}")
        else:
            self.reforzar_modelo(self.x, self.y, self.alimentacion, positivo=False)
            print(f"🕳️ {self.identificador} no encontró datos válidos en {self.posicion}")

        contexto = self.obtener_contexto_ambiental(datos_csv, aliados)
        self.log_memoria(
            entrada=self.alimentacion,
            resultado={
                "excrecion": self.excrecion,
                "recompensa": recompensa,
                "contexto": contexto
            },
            exitoso=recompensa > 0
        )

    def puede_reproducirse(self, umbral_recompensa=10):
        return self.recompensa_total >= umbral_recompensa

    def reproducirse(self, nuevo_id):
        nuevo_x = max(0, self.x + random.choice([-1, 0, 1]))
        nuevo_y = max(0, self.y + random.choice([-1, 0, 1]))
        nuevo_agente = Aritmetica(nuevo_id, nuevo_x, nuevo_y, self.z)
        nuevo_agente.memoria = self.memoria[-5:]
        nuevo_agente.alianzas = set(self.alianzas)
        print(f"🧬 {self.identificador} se ha reproducido como {nuevo_agente.identificador}")
        return nuevo_agente

__all__ = ["Aritmetica"]

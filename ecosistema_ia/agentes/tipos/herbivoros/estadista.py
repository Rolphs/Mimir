# estadista.py

import statistics

from ecosistema_ia.agentes.tipos.herbivoros.herbivoro_base import HerbivoroBase


class Estadista(HerbivoroBase):
    """Herbívoro que calcula estadísticas locales de su entorno."""

    def __init__(self, identificador, x, y, z):
        super().__init__(identificador, x, y, z, funcion="estadista")

    def actuar(self, territorio, otros_agentes=None):
        self.incrementar_edad()
        self.recibir_mensajes(territorio)

        datos_csv = territorio.get_csv(self.z)
        if not datos_csv:
            self.log_memoria(
                entrada="sin_datos",
                resultado={},
                exitoso=False,
            )
            return

        # Asegurar que la posición sea válida dentro del dataset
        self.x = max(0, min(self.x, len(datos_csv) - 1))
        fila_len = len(datos_csv[self.x]) if datos_csv[self.x] else 0
        self.y = max(0, min(self.y, fila_len - 1 if fila_len else 0))

        fila_ini = max(0, self.x - 1)
        fila_fin = min(len(datos_csv), self.x + 2)
        col_ini = max(0, self.y - 1)
        valores = []
        for i in range(fila_ini, fila_fin):
            fila = datos_csv[i]
            col_fin = min(len(fila), self.y + 2)
            for j in range(col_ini, col_fin):
                try:
                    valores.append(float(fila[j]))
                except (ValueError, TypeError, IndexError):
                    continue

        if valores:
            promedio = statistics.mean(valores)
            mediana = statistics.median(valores)
            desviacion = statistics.stdev(valores) if len(valores) > 1 else 0.0
            exitoso = True
        else:
            promedio = mediana = desviacion = 0.0
            exitoso = False

        stats = {
            "promedio": promedio,
            "mediana": mediana,
            "desviacion": desviacion,
        }

        self.log_memoria(
            entrada={"rango": (fila_ini, fila_fin, col_ini, self.y + 1)},
            resultado=stats,
            exitoso=exitoso,
        )
        self.broadcast_mensaje(territorio, stats, tipo="estadisticas")
        print(f"\U0001F4C8 {self.identificador} calculó {stats} en {self.posicion}")


__all__ = ["Estadista"]

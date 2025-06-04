# optimizacion_territorio.py

import csv
from pathlib import Path
import numpy as np
from sklearn.linear_model import LinearRegression
from ..config import LOGS_DIR

RUTA_LOG_CICLOS = LOGS_DIR / "ciclos.csv"

def cargar_datos_historicos(ruta=RUTA_LOG_CICLOS):
    ruta = Path(ruta)
    if not ruta.exists():
        print("📂 No se encontró historial de ciclos.")
        return []

    with ruta.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        datos = [row for row in reader]

    return datos


def estimar_ciclos_optimos(min_ciclos=5, max_ciclos=50, umbral_crecimiento=0.05):
    """
    Estima el número de ciclos óptimo observando el crecimiento de agentes en logs previos.
    :param min_ciclos: cantidad mínima garantizada.
    :param max_ciclos: máximo permitido para evitar loops infinitos.
    :param umbral_crecimiento: mínima tasa de crecimiento esperada para considerar que "vale la pena seguir".
    :return: cantidad estimada de ciclos.
    """
    datos = cargar_datos_historicos()
    if len(datos) < 5:
        print("📉 Datos insuficientes. Usando cantidad mínima de ciclos.")
        return min_ciclos

    ciclos = [int(d["ciclo"]) for d in datos]
    agentes = [int(d["total_agentes"]) for d in datos]

    if len(set(agentes)) <= 1:
        print("⚠️ No hubo variación en la población. Usando cantidad mínima de ciclos.")
        return min_ciclos

    X = np.array(ciclos).reshape(-1, 1)
    y = np.array(agentes)

    modelo = LinearRegression()
    modelo.fit(X, y)

    tasa_crecimiento = modelo.coef_[0]
    print(f"📈 Tasa de crecimiento estimada: {tasa_crecimiento:.3f}")

    if tasa_crecimiento < umbral_crecimiento:
        print("🧘 Crecimiento bajo. Recomendada una exploración corta.")
        return min_ciclos

    ciclos_estimados = int(min(max_ciclos, max(min_ciclos, y[-1] // 2)))
    print(f"🔮 Ciclos óptimos sugeridos: {ciclos_estimados}")
    return ciclos_estimados

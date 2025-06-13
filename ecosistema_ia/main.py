import csv
import importlib
import inspect
from datetime import datetime
from pathlib import Path

from ecosistema_ia.agentes.agente_base import AgenteBase

from ecosistema_ia.entorno.territorio import Territorio
from ecosistema_ia.entorno.paralelo import run_parallel
from ecosistema_ia.agentes.tipos.sublimes.metatron import Metatron
from ecosistema_ia.agentes.tipos.sublimes.mensajero import Mensajero
from ecosistema_ia.ml.optimizacion_territorio import estimar_ciclos_optimos
from ecosistema_ia.config import LOGS_DIR

def cargar_agentes_dinamicamente() -> list:
    """Importa e instancia automáticamente todas las clases de agentes.

    Cada agente recibe un identificador único en forma "XX-###" donde "XX" son
    las primeras dos letras del nombre de la clase y el número se incrementa de
    forma secuencial para cada instancia creada.
    """

    agentes = []
    contador = 1
    base_path = Path(__file__).resolve().parent / "agentes" / "tipos"
    clases_base = {"HerbivoroBase", "CarnivoroBase", "SublimeBase", "OmnivoroBase"}

    for tipo_path in base_path.iterdir():
        if not tipo_path.is_dir():
            continue

        for archivo in tipo_path.iterdir():
            if archivo.suffix != ".py" or archivo.name == "__init__.py":
                continue

            nombre_modulo = archivo.stem
            ruta_import = f"ecosistema_ia.agentes.tipos.{tipo_path.name}.{nombre_modulo}"

            try:
                modulo = importlib.import_module(ruta_import)

                for nombre_clase, clase in inspect.getmembers(modulo, inspect.isclass):
                    if clase.__module__ != ruta_import:
                        continue
                    if not issubclass(clase, AgenteBase):
                        continue
                    if nombre_clase in clases_base:
                        print(f"⚠️ Clase base {nombre_clase} ignorada")
                        continue
                    if hasattr(clase, "actuar") and callable(getattr(clase, "actuar")):
                        identificador = f"{nombre_clase[:2].upper()}-{contador:03d}"
                        try:
                            instancia = clase(identificador, 0, 0, 0)
                        except TypeError:
                            print(f"⚠️ {nombre_clase} requiere argumentos adicionales y será ignorada")
                            continue
                        agentes.append(instancia)
                        print(f"✅ Cargado dinámicamente: {identificador}")
                        contador += 1
            except Exception as e:
                print(f"❌ Error al cargar {ruta_import}: {e}")

    return agentes


def ejecutar_ciclo(agentes, territorio, paralelo=False):
    """Ejecuta un ciclo de simulación y devuelve la lista actualizada de agentes."""

    nuevos_agentes = []

    if paralelo:
        agentes = run_parallel(agentes, territorio)
    else:
        for agente in list(agentes):
            resultado = agente.actuar(territorio, otros_agentes=agentes)
            if isinstance(resultado, list):
                ids_actuales = {id(a) for a in agentes}
                ids_resultado = {id(a) for a in resultado}
                if ids_resultado.issubset(ids_actuales):
                    agentes = resultado
                else:
                    for nuevo in resultado:
                        if nuevo not in agentes:
                            agentes.append(nuevo)

    for agente in agentes:
        if hasattr(agente, "puede_reproducirse") and agente.puede_reproducirse():
            nuevo_id = f"{agente.identificador}-R{agente.edad}"
            nuevo = agente.reproducirse(nuevo_id)
            nuevos_agentes.append(nuevo)

    agentes.extend(nuevos_agentes)

    for agente in agentes:
        if hasattr(agente, "recombinar") and callable(getattr(agente, "recombinar")):
            nuevos = agente.recombinar(agentes)
            agentes.extend(nuevos)

    return agentes

def main(paralelo: bool = False):
    print("🌱 Iniciando el ecosistema Mimir...\n")

    # 1. Inicializar el Territorio
    territorio = Territorio()
    territorio.renderizar()

    # 2. Cargar agentes automáticamente desde las carpetas
    agentes = cargar_agentes_dinamicamente()

    # 3. Inicializar observadores
    metatron = Metatron()
    metatron_mensajes = Mensajero()

    # 4. Preparar archivo de log de ciclos
    log_file = LOGS_DIR / "ciclos.csv"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open(mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ciclo", "total_agentes", "timestamp"])

        # 5. Estimar ciclos evolutivos (mínimo 500)
        ciclos_estimados = max(500, estimar_ciclos_optimos())
        print(f"🔁 Ciclos a ejecutar (mínimo 500): {ciclos_estimados}")

        for ciclo in range(ciclos_estimados):
            print(f"\n🔁 Ciclo {ciclo + 1} | Agentes activos: {len(agentes)}")

            try:
                agentes = ejecutar_ciclo(agentes, territorio, paralelo=paralelo)

            except Exception as e:
                print(f"⚠️ Error durante el ciclo {ciclo + 1}: {e}")

            # Observadores
            metatron.observar(territorio, agentes, ciclo + 1)
            metatron_mensajes.observar(territorio, agentes, ciclo + 1)

            # Regulación del territorio
            agentes = territorio.regular(agentes, ciclo=ciclo + 1)

            # Registro de ciclo
            writer.writerow([ciclo + 1, len(agentes), datetime.now().isoformat()])

    print("\n✅ Ecosistema finalizado. Reporte de Metatrón generado.")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Simulación del ecosistema Mimir')
    parser.add_argument('--paralelo', action='store_true', help='Ejecutar agentes en paralelo')
    args = parser.parse_args()

    main(paralelo=args.paralelo)

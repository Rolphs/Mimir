import csv
import importlib
import inspect
from datetime import datetime
from pathlib import Path

from ecosistema_ia.entorno.territorio import Territorio
from ecosistema_ia.entorno.paralelo import run_parallel
from ecosistema_ia.agentes.tipos.sublimes.metatron import Metatron
from ecosistema_ia.agentes.tipos.sublimes.mensajero import Mensajero
from ecosistema_ia.ml.optimizacion_territorio import estimar_ciclos_optimos
from ecosistema_ia.config import LOGS_DIR

def cargar_agentes_dinamicamente() -> list:
    agentes = []
    base_path = Path(__file__).resolve().parent / "agentes" / "tipos"
    for tipo_path in base_path.iterdir():
        if not tipo_path.is_dir():
            continue
        for archivo in tipo_path.iterdir():
            if archivo.suffix == ".py" and archivo.name != "__init__.py":
                nombre_modulo = archivo.stem
                ruta_import = f"ecosistema_ia.agentes.tipos.{tipo_path.name}.{nombre_modulo}"
                try:
                    modulo = importlib.import_module(ruta_import)
                    for nombre_clase, clase in inspect.getmembers(modulo, inspect.isclass):
                        if hasattr(clase, "actuar") and callable(getattr(clase, "actuar")):
                            identificador = f"{nombre_clase[:2].upper()}-001"
                            instancia = clase(identificador, 0, 0, 0)
                            agentes.append(instancia)
                            print(f"✅ Cargado dinámicamente: {identificador}")
                            break
                except Exception as e:
                    print(f"❌ Error al cargar {ruta_import}: {e}")
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
                nuevos_agentes = []
                if paralelo:
                    agentes = run_parallel(agentes, territorio)
                else:
                    for agente in agentes:
                        agente.actuar(territorio, otros_agentes=agentes)

                for agente in agentes:
                    if hasattr(agente, "puede_reproducirse") and agente.puede_reproducirse():
                        nuevo_id = f"{agente.identificador}-R{agente.edad}"
                        nuevo = agente.reproducirse(nuevo_id)
                        nuevos_agentes.append(nuevo)

                agentes.extend(nuevos_agentes)

                # 🔁 Agentes con recombinación (como divisor_reproductor)
                for agente in agentes:
                    if hasattr(agente, "recombinar") and callable(getattr(agente, "recombinar")):
                        nuevos = agente.recombinar(agentes)
                        agentes.extend(nuevos)

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

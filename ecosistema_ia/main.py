import os
import csv
import importlib
import inspect
from datetime import datetime
from entorno.territorio import Territorio
from agentes.tipos.sublimes.metatron import Metatron
from agentes.tipos.sublimes.mensajero import MetatronMensajes
from ml.optimizacion_territorio import estimar_ciclos_optimos

def cargar_agentes_dinamicamente():
    agentes = []
    base_path = "agentes/tipos"
    for tipo in os.listdir(base_path):
        tipo_path = os.path.join(base_path, tipo)
        if not os.path.isdir(tipo_path):
            continue
        for archivo in os.listdir(tipo_path):
            if archivo.endswith(".py") and archivo != "__init__.py":
                nombre_modulo = archivo[:-3]
                ruta_import = f"agentes.tipos.{tipo}.{nombre_modulo}"
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

def main():
    print("🌱 Iniciando el ecosistema Mimir...\n")

    # 1. Inicializar el Territorio
    territorio = Territorio()
    territorio.renderizar()

    # 2. Cargar agentes automáticamente desde las carpetas
    agentes = cargar_agentes_dinamicamente()

    # 3. Inicializar observadores
    metatron = Metatron()
    metatron_mensajes = MetatronMensajes()

    # 4. Preparar archivo de log de ciclos
    with open("datos/logs/ciclos.csv", mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ciclo", "total_agentes", "timestamp"])

        # 5. Estimar ciclos evolutivos (mínimo 500)
        ciclos_estimados = max(500, estimar_ciclos_optimos())
        print(f"🔁 Ciclos a ejecutar (mínimo 500): {ciclos_estimados}")

        for ciclo in range(ciclos_estimados):
            print(f"\n🔁 Ciclo {ciclo + 1} | Agentes activos: {len(agentes)}")

            try:
                nuevos_agentes = []
                for agente in agentes:
                    agente.actuar(territorio, otros_agentes=agentes)
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
            metatron.observar(agentes, ciclo + 1)
            metatron_mensajes.observar_mensajes(territorio.buzon_mensajes, ciclo + 1)

            # Regulación del territorio
            agentes = territorio.regular(agentes, ciclo=ciclo + 1)

            # Registro de ciclo
            writer.writerow([ciclo + 1, len(agentes), datetime.now().isoformat()])

    print("\n✅ Ecosistema finalizado. Reporte de Metatrón generado.")

if __name__ == '__main__':
    main()
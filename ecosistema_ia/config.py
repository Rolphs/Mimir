# config.py

"""Configuración global del ecosistema Mimir."""

from pathlib import Path

# Número de ciclos evolutivos iniciales
CICLOS_INICIALES = 10

# Parámetros generales del ecosistema
TAMANO_TERRITORIO_X = 10
TAMANO_TERRITORIO_Y = 10
ARCHIVOS_CSV = ["data1.csv", "data2.csv"]  # Placeholder, deben existir

# Parámetros para agentes
NUM_AGENTES_INICIALES = 5

# Directorios base
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "datos"
DATASETS_DIR = BASE_DIR / "datasets"
LOGS_DIR = DATA_DIR / "logs"

# Rutas de archivos especiales
CSV_TERRITORIO_PATH = DATA_DIR / "territorio.csv"
CSV_METATRON_PATH = DATA_DIR / "metatron.csv"
CSV_METATRON_HEATMAP_PATH = DATA_DIR / "metatron_heatmap.csv"
CSV_METATRON_SEMANTICS_PATH = DATA_DIR / "metatron_semantics.csv"

# Bandera para controlar visualización en consola
MOSTRAR_INFO_CONSOLA = True

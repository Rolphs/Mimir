import os

BASE_PATH = "agentes/tipos"
OUTPUT_FILE = "agentes/agentes.txt"

def extraer_codigo_agentes():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as salida:
        for tipo in os.listdir(BASE_PATH):
            tipo_path = os.path.join(BASE_PATH, tipo)
            if not os.path.isdir(tipo_path):
                continue
            for archivo in os.listdir(tipo_path):
                if archivo.endswith(".py") and archivo != "__init__.py":
                    ruta_archivo = os.path.join(tipo_path, archivo)
                    salida.write(f"\n\n### {ruta_archivo} ###\n\n")
                    with open(ruta_archivo, "r", encoding="utf-8") as f:
                        salida.write(f.read())

if __name__ == "__main__":
    extraer_codigo_agentes()
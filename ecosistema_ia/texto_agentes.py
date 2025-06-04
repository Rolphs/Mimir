from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent / "agentes" / "tipos"
OUTPUT_FILE = Path(__file__).resolve().parent / "agentes" / "agentes.txt"

def extraer_codigo_agentes() -> None:
    with OUTPUT_FILE.open("w", encoding="utf-8") as salida:
        for tipo_path in BASE_PATH.iterdir():
            if not tipo_path.is_dir():
                continue
            for archivo in tipo_path.iterdir():
                if archivo.suffix == ".py" and archivo.name != "__init__.py":
                    salida.write(f"\n\n### {archivo} ###\n\n")
                    with archivo.open("r", encoding="utf-8") as f:
                        salida.write(f.read())

if __name__ == "__main__":
    extraer_codigo_agentes()

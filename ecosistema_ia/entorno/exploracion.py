"""Utilidades simples para inspeccionar datasets CSV."""

from pathlib import Path
from typing import List, Dict
import csv

from ..config import DATASETS_DIR


def listar_csvs(ruta: Path = DATASETS_DIR) -> List[Dict[str, int]]:
    """Devuelve información básica de los CSV disponibles en *ruta*.

    Cada elemento del resultado contiene el nombre del archivo y el número de
    filas y columnas que posee.
    """
    ruta = Path(ruta)
    info = []
    if not ruta.exists():
        print(f"⚠️ Ruta no encontrada: {ruta}")
        return info

    for csv_file in sorted(ruta.glob("*.csv")):
        try:
            with csv_file.open(newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader, [])
                row_count = sum(1 for _ in reader)
            info.append({
                "archivo": csv_file.name,
                "filas": row_count,
                "columnas": len(headers),
            })
        except Exception as e:
            print(f"⚠️ Error al procesar {csv_file}: {e}")
    return info


def previsualizar_csv(nombre: str, n: int = 5, ruta: Path = DATASETS_DIR) -> List[List[str]]:
    """Devuelve las primeras ``n`` filas de un CSV determinado."""
    csv_path = Path(ruta) / nombre
    filas: List[List[str]] = []
    if not csv_path.exists():
        print(f"⚠️ No se encontró el archivo: {csv_path}")
        return filas

    try:
        with csv_path.open(newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            encabezados = next(reader, [])
            filas.append(encabezados)
            for _ in range(n):
                row = next(reader, None)
                if row is None:
                    break
                filas.append(row)
    except Exception as e:
        print(f"⚠️ Error al leer {csv_path}: {e}")
    return filas


__all__ = ["listar_csvs", "previsualizar_csv"]

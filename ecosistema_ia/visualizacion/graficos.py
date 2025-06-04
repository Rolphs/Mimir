"""Funciones de visualización para el ecosistema Mimir."""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def generar_heatmap(ruta_csv: str, ciclo: int | None = None, output_dir: str | None = None) -> Path:
    """Genera una imagen de heatmap a partir de las posiciones registradas.

    Parameters
    ----------
    ruta_csv: str
        Ruta del CSV con columnas [ciclo, x, y, z, conteo].
    ciclo: int | None
        Si se indica, filtra los datos para ese ciclo específico.
    output_dir: str | None
        Carpeta donde guardar la imagen generada. Por defecto junto al CSV.

    Returns
    -------
    Path
        Ruta del archivo PNG creado.
    """

    csv_path = Path(ruta_csv)
    df = pd.read_csv(csv_path)
    if ciclo is not None:
        df = df[df["ciclo"] == ciclo]
    if df.empty:
        raise ValueError("No hay datos para generar el heatmap")

    max_x = int(df["x"].max()) + 1
    max_y = int(df["y"].max()) + 1
    matriz = np.zeros((max_x, max_y))
    for _, fila in df.iterrows():
        matriz[int(fila["x"]), int(fila["y"])] += fila["conteo"]

    plt.figure(figsize=(6, 5))
    plt.imshow(matriz, cmap="hot", origin="lower")
    plt.colorbar(label="Agentes")
    plt.xlabel("Y")
    plt.ylabel("X")

    out_dir = Path(output_dir) if output_dir else csv_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    nombre = f"heatmap_{ciclo if ciclo is not None else 'total'}.png"
    destino = out_dir / nombre
    plt.tight_layout()
    plt.savefig(destino)
    plt.close()
    return destino


__all__ = ["generar_heatmap"]


"""Visor de consola para resumir los logs de Metatrón."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from ecosistema_ia.config import (
    CSV_METATRON_HEATMAP_PATH,
    CSV_METATRON_SEMANTICS_PATH,
)


def _cargar_csv(ruta: Path) -> pd.DataFrame:
    """Cargar un CSV si existe, retornando un DataFrame vacío en caso contrario."""
    try:
        return pd.read_csv(ruta)
    except FileNotFoundError:
        print(f"⚠️ Archivo no encontrado: {ruta}")
        return pd.DataFrame()
    except Exception as exc:
        print(f"⚠️ Error al leer {ruta}: {exc}")
        return pd.DataFrame()


def _resumen_heatmap(df: pd.DataFrame) -> None:
    """Imprimir las coordenadas con mayor actividad registradas."""
    if df.empty:
        print("No hay datos de heatmap disponible.")
        return

    top = (
        df.groupby(["x", "y"])["conteo"].sum()
        .reset_index()
        .sort_values("conteo", ascending=False)
        .head(5)
    )
    print("\n🔆 Principales coordenadas observadas:")
    for _, fila in top.iterrows():
        x, y, conteo = int(fila["x"]), int(fila["y"]), int(fila["conteo"])
        print(f"  ({x}, {y}) → {conteo}")


def _resumen_semantica(df: pd.DataFrame) -> None:
    """Mostrar los tokens con mayor frecuencia."""
    if df.empty:
        print("No hay datos semánticos disponible.")
        return

    top = (
        df.groupby("token")["conteo"].sum().sort_values(ascending=False).head(5)
    )
    print("\n🔤 Tokens más comunes:")
    for token, conteo in top.items():
        print(f"  {token}: {int(conteo)}")


def mostrar_resumen() -> None:
    """Carga las métricas de Metatrón y las presenta de forma resumida."""
    heatmap_df = _cargar_csv(Path(CSV_METATRON_HEATMAP_PATH))
    sem_df = _cargar_csv(Path(CSV_METATRON_SEMANTICS_PATH))

    _resumen_heatmap(heatmap_df)
    _resumen_semantica(sem_df)


def main() -> None:
    """Punto de entrada del CLI."""
    mostrar_resumen()


if __name__ == "__main__":
    main()

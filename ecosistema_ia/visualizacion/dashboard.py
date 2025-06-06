"""Interactive dashboard utilities for the Mimir ecosystem."""

from pathlib import Path
import pandas as pd
import plotly.express as px

from ..config import CSV_METATRON_HEATMAP_PATH
from ..entorno.territorio import Territorio


def cargar_heatmap_interactivo(ruta_csv: str | None = None, ciclo: int | None = None):
    """Return a Plotly heatmap figure from Metatron logs.

    Parameters
    ----------
    ruta_csv : str | None
        Optional path to the CSV with columns [ciclo, x, y, z, conteo].
        Defaults to ``CSV_METATRON_HEATMAP_PATH``.
    ciclo : int | None
        Filter data for a specific cycle.

    Returns
    -------
    plotly.graph_objs.Figure
        Interactive heatmap figure.
    """
    csv_path = Path(ruta_csv) if ruta_csv else CSV_METATRON_HEATMAP_PATH
    df = pd.read_csv(csv_path)
    if ciclo is not None:
        df = df[df["ciclo"] == ciclo]
    if df.empty:
        raise ValueError("No hay datos para generar el heatmap interactivo")

    matriz = df.pivot_table(
        values="conteo", index="x", columns="y", aggfunc="sum", fill_value=0
    )
    fig = px.imshow(
        matriz,
        color_continuous_scale="Hot",
        origin="lower",
        labels={"x": "X", "y": "Y", "color": "Agentes"},
    )
    fig.update_layout(width=600, height=500, margin=dict(l=40, r=40, t=40, b=40))
    return fig


def estado_actual(territorio: Territorio) -> dict:
    """Return the current ecosystem metrics using ``Territorio.get_estado_json``."""
    return territorio.get_estado_json()


__all__ = ["cargar_heatmap_interactivo", "estado_actual"]

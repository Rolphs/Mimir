from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html

from ecosistema_ia.config import CSV_METATRON_HEATMAP_PATH, CSV_METATRON_SEMANTICS_PATH


def cargar_heatmap_dataframe(path: Path) -> pd.DataFrame:
    """Read the heatmap csv and return pivoted dataframe by x and y."""
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        return pd.DataFrame()
    if df.empty:
        return pd.DataFrame()
    pivot = (
        df.groupby(["x", "y"])["conteo"].sum().unstack(fill_value=0).sort_index()
    )
    return pivot


def cargar_semantica_dataframe(path: Path, top: int = 10) -> pd.DataFrame:
    """Return dataframe with top tokens and counts."""
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        return pd.DataFrame(columns=["token", "conteo"])
    if df.empty:
        return pd.DataFrame(columns=["token", "conteo"])
    agg = df.groupby("token")["conteo"].sum().sort_values(ascending=False).head(top)
    return agg.reset_index()


def crear_app() -> Dash:
    """Create the Dash application."""
    app = Dash(__name__)

    heatmap_df = cargar_heatmap_dataframe(CSV_METATRON_HEATMAP_PATH)
    sem_df = cargar_semantica_dataframe(CSV_METATRON_SEMANTICS_PATH)

    heatmap_fig = go.Figure()
    if not heatmap_df.empty:
        heatmap_fig.add_trace(
            go.Heatmap(
                z=heatmap_df.values,
                x=heatmap_df.columns.astype(str),
                y=heatmap_df.index.astype(str),
                colorscale="Hot",
            )
        )
        heatmap_fig.update_layout(title="Densidad de Agentes", xaxis_title="y", yaxis_title="x")

    bar_fig = go.Figure()
    if not sem_df.empty:
        bar_fig.add_trace(go.Bar(x=sem_df["token"], y=sem_df["conteo"]))
        bar_fig.update_layout(title="Tokens Semánticos Principales", xaxis_title="token", yaxis_title="conteo")

    app.layout = html.Div(
        [
            html.H1("Mimir Dashboard"),
            dcc.Graph(figure=heatmap_fig),
            dcc.Graph(figure=bar_fig),
        ]
    )
    return app


if __name__ == "__main__":
    app = crear_app()
    app.run(debug=True)

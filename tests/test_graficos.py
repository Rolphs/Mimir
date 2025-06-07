import pandas as pd
from ecosistema_ia.visualizacion.graficos import generar_heatmap


def test_generar_heatmap_creates_png(tmp_path):
    """generar_heatmap should create an output png file"""
    data = pd.DataFrame({
        "ciclo": [0, 0, 0],
        "x": [0, 1, 1],
        "y": [0, 1, 0],
        "z": [0, 0, 0],
        "conteo": [1, 2, 3],
    })
    csv_path = tmp_path / "heatmap.csv"
    data.to_csv(csv_path, index=False)

    output = generar_heatmap(str(csv_path))

    assert output.exists()
    assert output.suffix == ".png"

    # cleanup
    csv_path.unlink(missing_ok=True)
    output.unlink(missing_ok=True)

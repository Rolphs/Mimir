# Mimir Ecosystem

This repository contains an experimental ecosystem simulator written in Python.
Agents explore datasets, interact on a shared territory and produce logs that
can be analysed later.  Most of the code and comments are in Spanish.

## Structure

```
ecosistema_ia/
├── api/              # FastAPI server exposing the SPS REST API
├── agentes/          # agent implementations
├── datasets/         # CSV data used by the territory
├── datos/            # output logs generated during execution
├── entorno/          # territory management utilities
├── ml/               # basic machine learning helpers
└── visualizacion/    # stubs for future visual tools
```

The main entry point is `ecosistema_ia/main.py`. It loads agents dynamically
from the `agentes/tipos` directory, instantiates observers such as the
`Metatron` and `Mensajero` classes and runs a series of evolutionary cycles.

## Requirements

A minimal Conda environment specification is available in `environment.yml`.
It relies on **Python 3.11**, so make sure that version is available before
creating the environment:

```
conda env create -f environment.yml
conda activate mimir
```

The project only relies on standard libraries plus `pandas`, `numpy`,
`matplotlib`, `scikit-learn`, `fastapi`, `uvicorn` and `plotly`.

If you prefer a standard Python setup, the same dependencies are listed with
pinned versions in `requirements.txt`. This file mirrors the Conda
environment so both installation methods remain in sync. Install them with:

```
pip install -r requirements.txt
```

## Running

After installing the dependencies, run the ecosystem with:

```
python -m ecosistema_ia.main
```

Add the `--paralelo` flag to execute each agent in a separate process:

```
python -m ecosistema_ia.main --paralelo
```

Logs and CSV files will be written inside the `ecosistema_ia/datos` folder.

`Metatron` ahora también produce archivos `metatron_heatmap.csv` y
`metatron_semantics.csv`.  El primero resume la densidad de agentes por
coordenada, permitiendo generar mapas de calor con la función
`visualizacion.graficos.generar_heatmap`.  El segundo almacena tokens
relevantes para analizar la evolución semántica del ecosistema.

### Dashboard

Un tablero interactivo permite explorar visualmente la densidad de agentes y los tokens semánticos más frecuentes.  Tras generar los CSVs correspondientes, ejecútalo con:

```bash
python -m ecosistema_ia.visualizacion.dashboard
```

### Extracting agent code

The helper script `ecosistema_ia/texto_agentes.py` concatenates the source
of all agents into a single text file (`agentes/agentes.txt`) for inspection:

```
python ecosistema_ia/texto_agentes.py
```

### Inspecting datasets

Small helpers under `ecosistema_ia.entorno.exploracion` make it easy to look at
the CSVs bundled with the project.

```python
from ecosistema_ia.entorno.exploracion import listar_csvs, previsualizar_csv

for info in listar_csvs():
    print(f"{info['archivo']} -> {info['filas']} filas, {info['columnas']} columnas")

for row in previsualizar_csv("Episodes FAST.csv", n=3):
    print(row)
```

These utilities report the dimensions of each dataset and return a small sample
of rows for quick inspection.

### Dataset API

You can also query these helpers through the FastAPI server:

```bash
uvicorn ecosistema_ia.api.servidor:app --reload
```

* `GET /datasets` lists available CSV files.
* `GET /datasets/preview?name=<file>&n=<rows>` shows the first ``n`` rows of a CSV (``n`` defaults to ``5``).

## Testing

The test suite is based on **pytest**. After installing the project
dependencies, simply run:

```bash
pytest
```

`scikit-learn` must be available for the tests to succeed. The package is
already listed in `requirements.txt`, so make sure all dependencies are
installed before invoking `pytest`.
## White Paper Highlights

The "Mimir White Paper" describes a decentralized ecosystem where CSV files act as a multidimensional territory. Agents inhabit these files, modify them under evolutionary rules and compete for survival.

Key categories include **herbívoros** (data cleaners), **carnívoros** (which consume other agents) and **sublimes** (observers). Regulators such as the Calificador, Divisor Reproductor and Destructor balance the population.

A `Territorio` component maintains an immutable CSV log and adjusts parameters like agent density and mutation rate using machine learning. The early module **MAPS** (Motor de Adaptación Perceptual Simbótica) builds symbolic user profiles to adapt interfaces.

Agents evolve by rewards and natural selection, and visualisations progress from ASCII to interactive dashboards.
Read the full [white paper](docs/white_paper.md) for additional details.


## Symbolic Profile Styles API

The module `ecosistema_ia.sps` translates symbolic profile tokens to design
variables such as colours and fonts.  A small FastAPI server under
`ecosistema_ia/api` exposes an endpoint that receives a profile token and
returns the generated styles:

```bash
uvicorn ecosistema_ia.api.servidor:app --reload
```

Send a POST request to `/sps/styles` with a JSON body containing
`cromotipo`, `ritmo_cognitivo`, `arquetipo_narrativo` and `estilo_perceptual`.

The API responds with a dictionary of design variables that front-end
frameworks can consume.

## Notes

Most modules under `visualizacion/` remain lightweight, but now include a
utility to generate heatmaps from Metatron logs. The main focus continues to
be the command line simulation found in `main.py` and the SPS API.

## License

This project is licensed under the [MIT License](LICENSE).



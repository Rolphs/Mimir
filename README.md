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

A minimal Conda environment specification is available in `environment.yml`:

```
conda env create -f environment.yml
conda activate mimir
```

The project only relies on standard libraries plus `pandas`, `numpy`,
`matplotlib`, `scikit-learn`, `fastapi`, `uvicorn` and `plotly`.

## Running

After installing the dependencies, run the ecosystem with:

```
python -m ecosistema_ia.main
```

Logs and CSV files will be written inside the `ecosistema_ia/datos` folder.

`Metatron` ahora también produce archivos `metatron_heatmap.csv` y
`metatron_semantics.csv`.  El primero resume la densidad de agentes por
coordenada, permitiendo generar mapas de calor con la función
`visualizacion.graficos.generar_heatmap`.  El segundo almacena tokens
relevantes para analizar la evolución semántica del ecosistema.

### Extracting agent code

The helper script `ecosistema_ia/texto_agentes.py` concatenates the source
of all agents into a single text file (`agentes/agentes.txt`) for inspection:

```
python ecosistema_ia/texto_agentes.py
```
## White Paper Highlights

The "Mimir White Paper" describes a decentralized ecosystem where CSV files act as a multidimensional territory. Agents inhabit these files, modify them under evolutionary rules and compete for survival.

Key categories include **herbívoros** (data cleaners), **carnívoros** (which consume other agents) and **sublimes** (observers). Regulators such as the Calificador, Divisor Reproductor and Destructor balance the population.

A `Territorio` component maintains an immutable CSV log and adjusts parameters like agent density and mutation rate using machine learning. The early module **MAPS** (Motor de Adaptación Perceptual Simbótica) builds symbolic user profiles to adapt interfaces.

Agents evolve by rewards and natural selection, and visualisations progress from ASCII to interactive dashboards.


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
utility to generarate heatmaps from Metatron logs. The main focus continues to
be the command line simulation found in `main.py` and the SPS API.

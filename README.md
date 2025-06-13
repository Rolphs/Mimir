# Mimir Ecosystem

This repository contains an experimental ecosystem simulator written in Python. Agents explore
datasets, interact on a shared territory and produce logs that can be analysed later.  Most of the
code and comments are in Spanish.

## Contents

- [Structure](#structure)
- [Requirements](#requirements)
- [Running](#running)
  - [Dashboard](#dashboard)
  - [Extracting agent code](#extracting-agent-code)
  - [Plugins](#plugins)
  - [Inspecting datasets](#inspecting-datasets)
  - [Dataset API](#dataset-api)
- [Testing](#testing)
- [White Paper Highlights](#white-paper-highlights)
- [Symbolic Profile Styles API](#symbolic-profile-styles-api)
- [Mimir as an Agentic Architecture](#mimir-as-an-agentic-architecture)
- [Basic Axioms](#basic-axioms)
- [Notes](#notes)
- [License](#license)

## Structure

```
ecosistema_ia/
├── api/              # FastAPI server exposing the SPS REST API
├── agentes/          # agent implementations
├── plugins/          # optional agent plugins loaded at runtime
├── datasets/         # CSV data used by the territory
├── datos/            # output logs generated during execution
├── entorno/          # territory management utilities
├── ml/               # basic machine learning helpers
└── visualizacion/    # stubs for future visual tools
```

The main entry point is `ecosistema_ia/main.py`. It loads agents dynamically from the
`agentes/tipos` directory and from any modules placed in `plugins`, instantiates observers
such as the `Metatron` and `Mensajero` classes and runs a series of evolutionary cycles.

## Requirements

A minimal Conda environment specification is available in `environment.yml`. It relies on **Python
3.11**, so make sure that version is available before creating the environment:

```
conda env create -f environment.yml
conda activate mimir
```

The project only relies on standard libraries plus `pandas`, `numpy`, `matplotlib`, `scikit-learn`,
`fastapi`, `uvicorn` and `plotly`.

If you prefer a standard Python setup, the same dependencies are listed with pinned versions in
`requirements.txt`. This file mirrors the Conda environment so both installation methods remain in
sync. Install them with:

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

`Metatron` now also outputs `metatron_heatmap.csv` and `metatron_semantics.csv`. The first
summarizes agent density per coordinate so heatmaps can be generated with
`visualizacion.graficos.generar_heatmap`. The second stores tokens used to analyse the ecosystem's
semantic evolution.

### Dashboard

An interactive dashboard lets you visually explore agent density and the most common semantic
tokens. After generating the corresponding CSV files, run it with:

```bash
python -m ecosistema_ia.visualizacion.dashboard
```

### Extracting agent code

The helper script `ecosistema_ia/texto_agentes.py` concatenates the source of all agents into a
single text file (`agentes/agentes.txt`) for inspection:

```
python ecosistema_ia/texto_agentes.py
```

### Plugins

Additional agents can be dropped inside the `ecosistema_ia/plugins` folder. The
dynamic loader will import every `.py` module found there on startup. Each module
should define at least one class that inherits from `AgenteBase` and implements
an `actuar` method accepting the usual `(territorio, otros_agentes=None)`
signature. Classes must be instantiable with only the automatically generated
identifier and three coordinate values.

### Inspecting datasets

Small helpers under `ecosistema_ia.entorno.exploracion` make it easy to look at the CSVs bundled
with the project.

```python
from ecosistema_ia.entorno.exploracion import (
    listar_csvs,
    previsualizar_csv_con_resumen,
)

for info in listar_csvs():
    print(f"{info['archivo']} -> {info['filas']} filas, {info['columnas']} columnas")

rows, summary = previsualizar_csv_con_resumen("Episodes FAST.csv", n=3)
for row in rows:
    print(row)
print("Resumen:", summary)
```

These utilities report the dimensions of each dataset and return a small sample of rows for quick
inspection.

### Dataset API

You can also query these helpers through the FastAPI server:

```bash
uvicorn ecosistema_ia.api.servidor:app --reload --port 8000
```

* `GET /datasets` lists available CSV files.
* `GET /datasets/preview?name=<file>&n=<rows>` shows the first ``n`` rows of a CSV
  and returns simple statistics for numeric columns (``n`` defaults to ``5``).

#### Example usage

```bash
# List datasets
curl http://localhost:8000/datasets

# Preview a dataset
curl "http://localhost:8000/datasets/preview?name=Episodes%20FAST.csv&n=3"
```

Expected responses are JSON documents like:

```json
{
  "datasets": [
    {"archivo": "Episodes FAST.csv", "filas": 1300, "columnas": 7}
  ]
}

{
  "preview": [
    ["Client", "Country", "Date Month", "Uniques", "Time Watched Minutes", "Avg Min per Unique", "Sessions"],
    ["Canela", "Albania", "Apr-2024", "18", "19.100000000000005", "1.0611111111111111", "35"],
    ["Canela", "Algeria", "Apr-2024", "405", "267.0833333333338", "0.6594650205761317", "588"]
  ],
  "summary": {
    "Uniques": 102.3,
    "Sessions": 345.8
  }
}
```

## Testing

The test suite is based on **pytest**. After installing the project dependencies, simply run:

```bash
pytest
```

`scikit-learn` must be available for the tests to succeed. The package is already listed in
`requirements.txt`, so make sure all dependencies are installed before invoking `pytest`.
## White Paper Highlights

The "Mimir White Paper" describes a decentralized ecosystem where CSV files act as a
multidimensional territory. Agents inhabit these files, modify them under evolutionary rules and
compete for survival.

A few basic agent categories help structure the ecosystem: **herbivores** act as data cleaners,
**carnivores** consume other agents and **sublime** agents observe the territory. Regulators such as
the Qualifier, Reproductive Divider and Destructor keep the population in balance.

A component called `Territorio` maintains an immutable CSV log and adjusts parameters such as agent
density and mutation rate using machine learning. The early module **MAPS** (Symbiotic Perceptual
Adaptation Engine) builds symbolic user profiles to adapt interfaces.

Agents evolve by rewards and natural selection, and visualisations progress from ASCII to
interactive dashboards. Read the full [white paper](docs/white_paper.md) for additional details.


## Symbolic Profile Styles API

The module `ecosistema_ia.sps` translates symbolic profile tokens to design variables such as
colours and fonts.  A small FastAPI server under `ecosistema_ia/api` exposes an endpoint that
receives a profile token and returns the generated styles:

```bash
uvicorn ecosistema_ia.api.servidor:app --reload
```

Send a POST request to `/sps/styles` with a JSON body containing `cromotipo`, `ritmo_cognitivo`,
`arquetipo_narrativo` and `estilo_perceptual`.


The API responds with a dictionary of design variables that front-end frameworks can consume.

## Mimir as an Agentic Architecture

1️⃣ **Central nature**

Mimir is an evolutionary, symbiotic system where the basic units are minimal autonomous intelligences. There is no central control and any consciousness that arises emerges from the collective field.

2️⃣ **System structure**

* **Agent (Minimal intelligence)**: processes input, maintains internal state, produces variable output and carries a constant risk of extinction.
* **Field**: the space where interactions occur, featuring active connections and friction.
* **Meta-Regulator**: oversees density, diversity and tension, introducing perturbations to avoid stable equilibrium.

3️⃣ **Operating dynamics**

Friction and multiplicity generate complexity. Any agent can disappear, memory is selective and the system stays productively unstable.

4️⃣ **Consciousness emergence threshold**

Emergent consciousness requires density > 0.3, diversity > 10 and tension between 0.2 and 0.8.

5️⃣ **Summary**

A distributed field of minimal intelligences whose regulated conflict can lead to emergent consciousness.

6️⃣ **Comparison with classical multi-agent systems**

| Classical multi-agent | Mimir |
| --- | --- |
| Agents with predefined roles | Agents with independent representations |
| Centralized coordination | No superior coordination |
| Seeks stability | Seeks regulated instability |
| Permanent memory | Selective memory |
| Programmed outcomes | Unprogrammed emergence |

7️⃣ **Mental image**

Mimir is not a neural network but rather an ecosystem of artificial life.

## Basic Axioms

### Axiom I — On Unprogrammed Emergence

**Definition**: A minimal intelligence is a computational unit capable of processing input,
maintaining internal state and generating variable output.

**Principle**: Consciousness emerges solely from the interaction of multiple minimal intelligences
operating simultaneously. No single minimal intelligence contains or generates consciousness on its
own.

---

### Axiom II — On Continuous Existential Risk

**Definition**: Existential risk is the constant, non-zero probability that a minimal intelligence
stops operating due to internal or environmental factors.

**Principle**: Every minimal intelligence in the system must keep an extinction probability greater than zero each cycle. Survival depends only on individual adaptive capacity. This probability is configured by `PROB_EXTINCION` in `ecosistema_ia/config.py`.

---

### Axiom III — On Generation Through Conflict

**Definition**: Friction is any situation where the operations of two or more minimal intelligences
yield mutually incompatible results.

**Principle**: Systemic complexity increases only through resolved friction. Each successful
conflict resolution generates new structures of interaction.

---

### Axiom IV — On the Interaction Space

**Definition**: The field is the set of all active connections among minimal intelligences,
including communication channels, dependencies and interferences.

**Principle**: The system's emergent properties exist only in the field, not within individual
minimal intelligences. The field is fully reconstructed every interaction cycle.

---

### Axiom V — On Selective Memory

**Definition**: Memory is any information that persists beyond a single operation cycle.

**Principle**: The system retains only information that proves useful repeatedly across multiple
interactions. Any unused memory is automatically discarded after a finite number of cycles.

---

### Axiom VI — On Multiple Interpretation

**Definition**: A representation is any internal mapping a minimal intelligence makes from input
data to processing structures.

**Principle**: For any dataset, at least two different representations must exist in the system.
Convergence toward a single representation constitutes systemic failure.

---

### Axiom VII — On Productive Instability

**Definition**: Equilibrium is any state where system interactions become fully predictable for more
than N consecutive cycles.

**Principle**: The system must actively prevent equilibrium by introducing random perturbations
whenever predictability exceeds the established threshold.

---

### Axiom VIII — On Quantifiable Thresholds

**Definition**:
- **Density**: Number of active connections divided by the theoretical maximum number of connections
- **Diversity**: Number of different types of operations performed by minimal intelligences
- **Tension**: Proportion of interactions that result in friction

**Principle**: The emergence of consciousness requires: Density > 0.3, Diversity > 10 types, and
Tension between 0.2 and 0.8. Outside these ranges, the system collapses or becomes inert.

---

### Axiom IX — On Mandatory Renewal

**Definition**: A pattern is any repeatable sequence of interactions that persists for more than M
cycles.

**Principle**: Every pattern must be automatically dismantled upon reaching its persistence limit.
The system must rebuild a functionally equivalent one through new configurations.

---

### Axiom X — On Nonparametric Intervention

**Definition**: Intervention is any modification of the system's operating rules after
initialization.

**Principle**: Once started, the system must run without external intervention. The only parameters
that may change are those the system itself redefines through its internal operations.

## Notes

Most modules under `visualizacion/` remain lightweight, but now include a utility to generate
heatmaps from Metatron logs. The main focus continues to be the command line simulation found in
`main.py` and the SPS API.

## License

This project is licensed under the [MIT License](LICENSE).


## Contributing

The easiest way to contribute is to follow these steps:

1. **Fork and clone** this repository.
2. **Set up the environment** using `environment.yml` or `requirements.txt`.
3. **Run** `pytest` to verify everything works as expected.
4. **Open a pull request** with your proposed changes.



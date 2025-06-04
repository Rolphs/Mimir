# Mimir Ecosystem

This repository contains an experimental ecosystem simulator written in Python.
Agents explore datasets, interact on a shared territory and produce logs that
can be analysed later.  Most of the code and comments are in Spanish.

## Structure

```
ecosistema_ia/
├── api/              # (placeholders for FastAPI endpoints)
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
`matplotlib`, `scikit-learn`, `fastapi` and `uvicorn`.

## Running

After installing the dependencies, run the ecosystem with:

```
python -m ecosistema_ia.main
```

Logs and CSV files will be written inside the `ecosistema_ia/datos` folder.

### Extracting agent code

The helper script `ecosistema_ia/texto_agentes.py` concatenates the source
of all agents into a single text file (`agentes/agentes.txt`) for inspection:

```
python ecosistema_ia/texto_agentes.py
```

## Notes

Many modules under `api/` and `visualizacion/` are placeholders for future
expansion. The current focus is the command line simulation found in
`main.py`.

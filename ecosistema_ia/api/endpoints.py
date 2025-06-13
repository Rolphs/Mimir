"""FastAPI endpoints for the SPS library."""

from fastapi import APIRouter
from pydantic import BaseModel
from ecosistema_ia.sps import SymbolicProfile, generate_styles
from ecosistema_ia.entorno.exploracion import (
    listar_csvs,
    previsualizar_csv,
    previsualizar_csv_con_resumen,
)

router = APIRouter()


class ProfileToken(BaseModel):
    cromotipo: str
    ritmo_cognitivo: str
    arquetipo_narrativo: str
    estilo_perceptual: str


@router.post("/sps/styles")
def get_styles(token: ProfileToken):
    """Return design variables for a symbolic profile token."""
    profile = SymbolicProfile(**token.dict())
    styles = generate_styles(profile.to_token())
    return {"styles": styles}


@router.get("/datasets")
def get_datasets():
    """Return a list of available CSV datasets."""
    return {"datasets": listar_csvs()}


@router.get("/datasets/preview")
def preview_dataset(name: str, n: int = 5):
    """Return the first ``n`` rows and basic stats of the selected CSV file."""
    rows, summary = previsualizar_csv_con_resumen(name, n=n)
    return {"preview": rows, "summary": summary}

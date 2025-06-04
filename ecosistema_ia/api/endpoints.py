"""FastAPI endpoints for the SPS library."""

from fastapi import APIRouter
from pydantic import BaseModel
from ecosistema_ia.sps import SymbolicProfile, generate_styles

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

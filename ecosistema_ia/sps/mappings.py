"""Simple mapping from symbolic profile dimensions to design variables."""

from typing import Dict

# Example mapping dictionaries; in real use these could be loaded from a database
CROMOTIPO_COLOR = {
    "sol": "#FFD700",
    "luna": "#B0C4DE",
    "tierra": "#8FBC8F",
}

RITMO_TIPOGRAFIA = {
    "lento": "serif",
    "medio": "sans-serif",
    "rapido": "monospace",
}

ARQUETIPO_ICONO = {
    "explorador": "compass",
    "cuidador": "heart",
    "forajido": "skull",
}

ESTILO_ANIMACION = {
    "visual": "fade",
    "auditivo": "pulse",
    "kinestesico": "bounce",
}

def generate_styles(token: Dict[str, str]) -> Dict[str, str]:
    """Return design variables derived from a symbolic profile token."""
    return {
        "color_primario": CROMOTIPO_COLOR.get(token.get("cromotipo"), "#FFFFFF"),
        "fuente_base": RITMO_TIPOGRAFIA.get(token.get("ritmo_cognitivo"), "sans-serif"),
        "icono": ARQUETIPO_ICONO.get(token.get("arquetipo_narrativo"), "star"),
        "animacion": ESTILO_ANIMACION.get(token.get("estilo_perceptual"), "fade"),
    }

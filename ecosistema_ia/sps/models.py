from dataclasses import dataclass
from typing import Dict

@dataclass
class SymbolicProfile:
    """Basic symbolic profile token."""
    cromotipo: str
    ritmo_cognitivo: str
    arquetipo_narrativo: str
    estilo_perceptual: str

    def to_token(self) -> Dict[str, str]:
        return {
            "cromotipo": self.cromotipo,
            "ritmo_cognitivo": self.ritmo_cognitivo,
            "arquetipo_narrativo": self.arquetipo_narrativo,
            "estilo_perceptual": self.estilo_perceptual,
        }
